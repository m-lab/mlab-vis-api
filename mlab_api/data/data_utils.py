# -*- coding: utf-8 -*-

import struct
import logging

from gcloud import bigtable
from gcloud.bigtable import happybase
from oauth2client.client import GoogleCredentials

URL_KEY_DELIM = "+"
BIGTABLE_KEY_DELIM = "|"

def init_pool(app_config):
    '''
    Setup Connection
    From the documentation:
    Creating a Connection object is a heavyweight operation;
     you should create a single Connection and
     share it among threads in your application.
    '''

    credentials = GoogleCredentials.get_application_default()
    connection_pool = None

    if 'GOOGLE_PROJECT_ID' and 'BIGTABLE_INSTANCE' in app_config:
        try:
            client = bigtable.Client(project=app_config['GOOGLE_PROJECT_ID'],
                                     admin=True, credentials=credentials)

            instance = client.instance(app_config['BIGTABLE_INSTANCE'])

            size = 10
            if 'BIGTABLE_POOL_SIZE' in app_config:
                size = app_config['BIGTABLE_POOL_SIZE']

            connection_pool = happybase.pool.ConnectionPool(size, instance=instance)
        except Exception as err:  #pylint: disable=W0703
            logging.exception("ERROR: Could not make connection")
            logging.exception(err)
    else:
        logging.warning('WARNING: no connection made')
    return connection_pool

def get_location_key_fields(location_id, table_config):
    '''
    Returns an array of strings representing the portions of the  row
    key for the location fields
    '''

    location_fields = location_id.split(URL_KEY_DELIM)
    return get_key_fields(location_fields, table_config)

def get_key_fields(field_ids, table_config):
    '''
    Given a list of key field ids,
    return list of fields with appropriate padding and transformations.
    matching between field id and table config's row_keys is done by
    list position.
    '''
    key_fields = []
    for index, field in enumerate(field_ids):
        # TODO: should we check the names?
        field_config = table_config['row_keys'][index]
        key_length = field_config['length']
        key_fields.append(field.ljust(key_length))

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

def get_client_isp_fields(client_isp_id, table_config):
    '''
    Returns an array of strings representing portions of the row
    key for the Client ISP

    Args:
    client_isp_id - ASN Number
    '''

    client_parts = client_isp_id.split(URL_KEY_DELIM)
    client_isp_fields = []
    field_names = ['client_asn_number']

    for index, field_name in enumerate(field_names):
        field_config = [x for x in table_config['row_keys'] if x['name'] == field_name][0]
        key_length = field_config['length']
        client_isp_fields.append(client_parts[index].ljust(key_length))

    return client_isp_fields


def decode_value(value, col_type):
    '''
    Decode a given value, based on its given type
    '''
    new_value = value
    if col_type == 'double':
        try:
            new_value = round(struct.unpack('>d', value)[0], 3)
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
    else:
        try:
            new_value = value.encode('utf-8')
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
        if name in col_configs:
            col_type = col_configs[name]['type']
        else:
            logging.warning('WARNING: missing in col configs: ' + name)

        decoded_value = decode_value(value, col_type)
        if keep_family:
            parsed[family][name] = decoded_value
        else:
            parsed[name] = decoded_value

    return parsed

def format_metric_data(raw_data):
    '''
    Convert metric raw data list into format to send back to client
    '''
    results = {"results": [], "meta":{}}
    # Meta can be taken from first result

    formated_metrics = []
    for metric in raw_data:
        # special cases for date and hour
        if 'date' in metric['meta']:
            metric['data']['date'] = metric['meta']['date']
        if 'hour' in metric['meta']:
            metric['data']['hour'] = metric['meta']['hour']
        formated_metrics.append(metric['data'])
    results["results"] = formated_metrics

    if len(raw_data) > 0:
        meta = raw_data[0]["meta"]
        meta.pop('date', None)
        meta.pop('hour', None)

        results["meta"] = meta

    return results
