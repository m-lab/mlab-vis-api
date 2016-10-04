# -*- coding: utf-8 -*-
'''
Utilities to help with connecting and communicating with BigTable
'''

import logging

from gcloud import bigtable
from gcloud.bigtable import happybase
from gcloud.bigtable.row_filters import FamilyNameRegexFilter
from oauth2client.client import GoogleCredentials

import mlab_api.data.data_utils as du
from mlab_api.stats import statsd
from mlab_api.sort_utils import sort_by_count

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

def scan_table(table_config, pool, prefix="", start_key="", end_key="", **kwargs):
    '''
    Abstracts table scan - performing the connection to table via
    connection pool and automatic retry of failed scans.
    Additional named arguments are passed to scan call.
    '''
    table_id = table_config['bigtable_table_name']

    # build table query parameters.
    # if prefix is present, use that.
    # else, use start / end key
    params = {}
    if len(prefix) > 0:
        params = {"row_prefix": prefix.encode('utf-8')}
    elif len(start_key) > 0:
        params = {"row_start": start_key.encode('utf-8'), "row_stop": end_key.encode('utf-8')}

    params.update(kwargs)

    logging.info("querying: %s", table_id)
    logging.info("start_key: %s", start_key)
    logging.info("end_key: %s", end_key)
    logging.info("prefix: %s", prefix)
    logging.info("params %s", str(params))

    results = []

    # Hack to allow for reattempts
    for attempt in range(10):
        try:
            with pool.connection(timeout=5) as connection:
                connection.open()
                table = connection.table(table_id)

                for _, data in table.scan(**params):
                    results.append(du.parse_row(data, table_config.columns))
        except Exception as err: #pylint: disable=W0703
        # TODO: use specific exception catch.
            logging.warning("Failed query attempt %s", str(attempt))
            logging.warning(err)
        else:
            break
    else:
        results = []
    logging.info("result size %s", str(len(results)))
    return results

def get_row(table_config, pool, row_key, **kwargs):
    '''
    Retrieve a single result from a table
    '''
    table_id = table_config['bigtable_table_name']

    logging.info("querying: %s", table_id)
    logging.info("row_key: %s", row_key)
    row = {}
    # Hack to allow for reattempts
    for attempt in range(10):
        try:
            with pool.connection(timeout=5) as connection:
                connection.open()
                table = connection.table(table_id)

                data = table.row(row_key, **kwargs)
                row = du.parse_row(data, table_config.columns)
        except Exception as err: #pylint: disable=W0703
        # TODO: use specific exception catch.
            logging.warning("Failed query attempt %s", str(attempt))
            logging.warning(err)
        else:
            break
    else:
        row = {}
    return row

def get_time_metric_results(key_fields, pool, timebin, starttime, endtime, table_config, metric_name):
    # get startkey and endkey prefixed with key_fields
    start_key, end_key = du.get_full_time_keys(key_fields, timebin, starttime, endtime, table_config)

    # Prepare to query the table
    results = []
    with statsd.timer('{0}.metric.scan_table'.format(metric_name)):
        results = scan_table(table_config, pool, start_key=start_key, end_key=end_key)

    formatted = {}
    with statsd.timer('{0}.metric.format_data'.format(metric_name)):
        # format output for API
        formatted = du.format_metric_data(results, starttime=starttime, endtime=endtime, agg=timebin)
    return formatted

def get_list_table_results(key_fields, pool, include_data, table_config, metric_name):

    key_fields = du.BIGTABLE_KEY_DELIM.join(key_fields)

    params = {"prefix":key_fields}
    if not include_data:
        params["filter"] = FamilyNameRegexFilter('meta')

    results = []
    with statsd.timer('{0}.listtable.scan_table'.format(metric_name)):
        results = scan_table(table_config, pool, **params)

    sorted_results = []
    with statsd.timer('{0}.listtable.sort_results'):
        sorted_results = sorted(results, key=sort_by_count, reverse=True)
    return sorted_results
