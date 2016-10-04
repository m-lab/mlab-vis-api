# -*- coding: utf-8 -*-
'''
Utilities to help with data transformations
'''

import struct
import logging

from mlab_api.constants import TABLE_KEYS
from datetime import datetime
from dateutil.relativedelta import relativedelta

TIME_FORMATS = {"day": "%Y-%m-%d",
                "month": "%Y-%m",
                "year": "%Y"}

RELATIVE_NAMES = {"day": "days", "month": "months", "year": "years"}

URL_KEY_DELIM = "+"
BIGTABLE_KEY_DELIM = "|"

def list_table(target_id, scope_id = None):
    '''
    Return name of a list table given what entity you are targeting
    and what entity scopes / facets the target.
    target_id = [locations, servers, clients]
    scope_id = [locations, servers, clients]
    '''
    names = [TABLE_KEYS[tid] for tid in [scope_id, target_id] if tid]
    return "_".join(names) + "_list"

def search_table(target_id):
    '''
    Return name of table for searching target
    target_id = [locations, servers, clients]
    '''
    return TABLE_KEYS[target_id] + "_search"


def get_location_key_fields(location_id, table_config):
    '''
    Returns an array of strings representing the portions of the  row
    key for the location fields
    '''

    location_fields = location_id.split(URL_KEY_DELIM)
    return get_key_fields(location_fields, table_config)


def get_key_field(field, index, table_config):
    '''
    Return padded field ready to be used in bigtable key
    Amount of padding is read from table_config, based on the index
    of the field
    '''
    # TODO: should we check the names?
    field_config = table_config['row_keys'][index]
    key_length = field_config['length']
    return field.ljust(key_length)

def get_key_fields(field_ids, table_config):
    '''
    Given a list of key field ids,
    return list of fields with appropriate padding and transformations.
    matching between field id and table config's row_keys is done by
    list position.
    '''
    key_fields = []
    for index, field in enumerate(field_ids):
        key_fields.append(get_key_field(field, index, table_config))
    return key_fields

def get_time_key_fields(time_value, time_aggregation, table_config):
    '''
    Returns an array of strings representing the portions of the  row
    key for the time fields
    '''
    times = time_value.split(URL_KEY_DELIM)

    time_key_fields = []
    field_names = ['date']
    if 'hour' in time_aggregation:
        field_names.append('hour')
        if len(times) == 1:
            # we are missing an hour value
            times.append('0')

    for index, field_name in enumerate(field_names):
        field_config = [x for x in table_config['row_keys'] if x['name'] == field_name][0]
        key_length = field_config['length']
        time_key_fields.append(times[index].ljust(key_length))

    return time_key_fields

def get_full_time_keys(key_fields, timebin, starttime, endtime, table_config):
    '''
    Helper function that combines functions needed to create
    a full start and end time key used to query metrics.
    '''

    starttime_fields = get_time_key_fields(starttime, timebin, table_config)

    inclusive_endtime = add_time(endtime, 1, timebin)
    endtime_fields = get_time_key_fields(inclusive_endtime, timebin, table_config)

    start_key = BIGTABLE_KEY_DELIM.join(key_fields + starttime_fields)

    end_key = BIGTABLE_KEY_DELIM.join(key_fields + endtime_fields)

    return (start_key, end_key)


def decode_value(value, col_type, options={}):
    '''
    Decode a given value, based on its given type
    '''
    new_value = value
    if col_type == 'double':
        shouldRound = True
        if 'round' in options:
            shouldRound = options['round']
        try:
            if shouldRound:
                new_value = round(struct.unpack('>d', value)[0], 3)
            else:
                new_value = struct.unpack('>d', value)[0]
        except Exception as err:  #pylint: disable=W0703
            logging.exception("Double Conversion Error")
            logging.exception(str(err))
            new_value = None
    elif col_type == 'integer':
        try:
            new_value = int(value)
        except Exception as err:  #pylint: disable=W0703
            logging.exception("Integer Conversion Error")
            logging.exception(str(err))
            new_value = None
    elif col_type == 'integer_list':
        values = value.split(',')
        try:
            new_value = [int(value) for value in values]
        except Exception as err:  #pylint: disable=W0703
            logging.exception("Integer Conversion Error")
            logging.exception(str(err))
            new_value = []
    else:
        try:
            new_value = value.decode('utf-8').encode('utf-8')
        except Exception as err:  #pylint: disable=W0703
            logging.warning("String Conversion Error")
            logging.warning(str(err))
            new_value = value
    return new_value

def parse_row(row, col_configs, keep_family=True):
    '''
    Convert Hbase results back to sane dict
    '''
    parsed = {}

    for key, value in row.iteritems():
        (family, name) = key.split(":")

        if keep_family:
            if family not in parsed:
                parsed[family] = {}

        col_type = 'string'
        options = {}
        if name in col_configs:
            col_type = col_configs[name]['type']
            if 'options' in col_configs[name]:
                options = col_configs[name]['options']
        else:
            logging.warning('WARNING: missing in col configs: ' + name)

        decoded_value = decode_value(value, col_type,  options)
        if keep_family:
            parsed[family][name] = decoded_value
        else:
            parsed[name] = decoded_value

    return parsed

def add_time(basetime_string, amount, time_aggregation):
    '''
    Add amount of time to a base time.
    Base time is expected to be a string.
    time_aggregation indicates how to parse it, and
    what the metric of 'amount' is.

    time_aggregation can be one of: day, month, year.
    '''
    # HACK around hour times
    basetime_string = basetime_string.split(URL_KEY_DELIM)[0]
    date_field = time_aggregation.split("_")[0]
    time_format = get_time_format(date_field)

    basetime = datetime.strptime(basetime_string, time_format)
    relativename = get_relative_time_name(date_field)

    new_time = basetime + relativedelta(**{relativename: amount})
    return new_time.strftime(time_format)


def get_time_format(date_field):
    '''
    Get time format for dates in day, month, or year format
    '''
    return TIME_FORMATS[date_field]

def get_relative_time_name(date_field):
    '''
    Get name for day, month, year - for use with relativetime
    '''
    return RELATIVE_NAMES[date_field]

def create_date_range(starttime, endtime, time_aggregation):
    '''
    Return list of date strings in the format
    appropriate for the `delta` input.
    time_aggregation: one of day, month, year.
    Date range list is inclusive of start and end time.
    '''

    def diff_day(d1, d2):
        '''
        Returns integer representing number of days between d1 and d2
        '''
        return (d2 - d1).days + 1

    def diff_month(d1, d2):
        '''
        Returns integer representing number of months between d1 and d2
        '''
        return ((d2.year - d1.year) * 12 + d2.month - d1.month) + 1

    def diff_year(d1, d2):
        '''
        Returns integer representing number of years between d1 and d2
        '''
        return (d2.year - d1.year) + 1

    def create_hour_range():
        '''
        Returns an array of strings from '00' to '23'
        '''
        hours = []
        for n in range(24):
            hours.append(str(n).zfill(2))
        return hours

    # HACK some insider knowledge to know the
    # hour names are split by a _
    time_fields = time_aggregation.split("_")
    date_aggregation = time_fields[0]

    hours = None
    if len(time_fields) > 1 and time_fields[-1] == 'hour':
        hours = create_hour_range()

    time_format = get_time_format(date_aggregation)
    start = datetime.strptime(starttime, time_format)
    end = datetime.strptime(endtime, time_format)

    diff_time = 0
    relativename = get_relative_time_name(date_aggregation)

    if date_aggregation == 'day':
        diff_time = diff_day(start, end)
    elif date_aggregation == 'month':
        diff_time = diff_month(start, end)
    elif date_aggregation == 'year':
        diff_time = diff_year(start, end)

    # HACK this should probably be a generator...
    dates = []
    for n in range(diff_time):
        # use relativedelta to add appropriate amounts.
        mid_date = start + relativedelta(**{relativename:n})
        mid_date_str = mid_date.strftime(time_format)

        new_dates = []

        # add in hours if necessary
        if hours:
            new_dates = [mid_date_str + "+" + hour for hour in hours]
        else:
            new_dates = [mid_date_str]

        # combine with previous dates
        dates += new_dates

    return dates


def format_metric_data(raw_data, starttime, endtime, agg):
    '''
    Convert metric raw data list into format to send back to client
    '''

    starttime = starttime.split(URL_KEY_DELIM)[0]
    endtime = endtime.split(URL_KEY_DELIM)[0]

    # Put date and hour in data
    # create dictionary out of returned values.
    keyed_metrics = {}
    for metric in raw_data:
        date_key = ""
        if 'date' in metric['meta']:
            metric['data']['date'] = metric['meta']['date']
            date_key += metric['data']['date']

        if 'hour' in metric['meta']:
            metric['data']['hour'] = metric['meta']['hour']
            date_key += "+" + metric['data']['hour']

        # HACK: if we don't have date or hour,
        # this mapping will fail.
        keyed_metrics[date_key] = metric['data']

    # Iterate through all dates that should be present
    all_dates = create_date_range(starttime, endtime, agg)

    formated_metrics = []
    for date in all_dates:
        # if the date is in the results,
        # use that - else put in a blank.
        if date in keyed_metrics:
            formated_metrics.append(keyed_metrics[date])
        else:
            # HACK: this + split is using knowledge of how
            # create_date_range makes its date + hour values.
            key_fields = date.split('+')
            blank = {'date': key_fields[0]}
            if len(key_fields) > 1:
                blank['hour'] = key_fields[1]
            formated_metrics.append(blank)

    results = {"results": [], "meta":{}}
    results["results"] = formated_metrics

    if len(raw_data) > 0:
        meta = raw_data[0]["meta"]
        meta.pop('date', None)
        meta.pop('hour', None)

        results["meta"] = meta

    return results
