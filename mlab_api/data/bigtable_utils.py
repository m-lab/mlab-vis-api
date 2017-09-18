# -*- coding: utf-8 -*-
# pylint: disable=unused-argument
'''
Utilities to help with connecting and communicating with BigTable
'''

import logging
import os

#pylint: disable=no-name-in-module, relative-import
from google.cloud import bigtable
from google.cloud import happybase
from google.cloud.bigtable.row_filters import FamilyNameRegexFilter
from google.oauth2 import service_account

import mlab_api.data.data_utils as du
from mlab_api.sort_utils import sort_by_count

def init_pool():
    '''
    Setup Connection
    From the documentation:
    Creating a Connection object is a heavyweight operation;
     you should create a single Connection and
     share it among threads in your application.
    '''

    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    connection_pool = None
    project_id = os.environ.get("PROJECT")
    bigtable_instance = os.environ.get("BIGTABLE_INSTANCE")
    bigtable_pool_size = os.environ.get("BIGTABLE_POOL_SIZE")

    if project_id and bigtable_instance:
        try:
            client = bigtable.Client(project=project_id,
                                     admin=True, credentials=credentials)

            instance = client.instance(bigtable_instance)

            size = int(bigtable_pool_size) if bigtable_pool_size else 10

            connection_pool = happybase.pool.ConnectionPool(size,
                                                            instance=instance)
            logging.info("Connection made to %s for project %s",
                         bigtable_instance, project_id)
        except Exception as err:  #pylint: disable=W0703
            logging.exception("ERROR: Could not make connection")
            logging.exception(err)
    else:
        logging.warning('WARNING: no connection made')
    return connection_pool

def scan_table(table_config, pool, prefix="", start_key="", end_key="",
               **kwargs):
    '''
    Abstracts table scan - performing the connection to table via
    connection pool and automatic retry of failed scans.
    Additional named arguments are passed to scan call.

    table_config = configuration object for a table to scan.
    pool = bigtable connection pool.
    prefix = prefix key scan with this value.
    start_key = alternative to prefix, start_key & stop_key allow for
        scaning ranges.
    stop_key = alternative to prefix, start_key & stop_key allow for
        scaning ranges.
    kwargs = additional keyword arguments passed directly to the scan operation.
    '''
    table_id = table_config['bigtable_table_name']

    # build table query parameters.
    # if prefix is present, use that.
    # else, use start / end key
    params = {}
    if prefix:
        params = {"row_prefix": prefix.encode('utf-8')}
    elif start_key:
        params = {
            "row_start": start_key.encode('utf-8'),
            "row_stop": end_key.encode('utf-8')
        }

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
        # TODO: use specific exception catch.
        except Exception as err: #pylint: disable=W0703
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

    table_config = configuration object for a table to scan.
    pool = bigtable connection pool.
    row_key = key of row to get.
    kwargs = additional keyword arguments passed directly to query.
    '''
    table_id = table_config['bigtable_table_name']
    row_key = row_key.encode('utf-8')

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
        # TODO: use specific exception catch.
        except Exception as err: #pylint: disable=W0703
            logging.warning("Failed query attempt %s", str(attempt))
            logging.warning(err)
        else:
            break
    else:
        row = {}
    return row

def get_time_metric_results(key_fields, pool, timebin, starttime, endtime,
                            table_config, metric_name):
    '''
    Helper to query table and create results for time based metrics

    key_fields = array of key fields.
    pool = connection pool.
    starttime = formatted start time of metric query.
    endtime = formatted end time of metric query.
    table_config = configuration file for table to query from.
    '''
    # get startkey and endkey prefixed with key_fields
    start_key, end_key = du.get_full_time_keys(key_fields, timebin, starttime,
                                               endtime, table_config)

    # Prepare to query the table
    results = []
    results = scan_table(table_config, pool, start_key=start_key,
                         end_key=end_key)

    formatted = {}
    # format output for API
    formatted = du.format_metric_data(results, starttime=starttime,
                                      endtime=endtime, agg=timebin)
    return formatted

def get_list_table_results(key_fields, pool, include_data, table_config,
                           metric_name):
    '''
    Helper to query table and create results for list based results

    key_fields = array of key fields.
    pool = connection pool.
    include_data = boolean indicating if data attributes should be
        included in results.
    table_config = configuration file for table to query from.
    '''

    key_fields = du.BIGTABLE_KEY_DELIM.join(key_fields)

    params = {"prefix":key_fields}
    if not include_data:
        params["filter"] = FamilyNameRegexFilter('meta')

    results = []
    results = scan_table(table_config, pool, **params)

    sorted_results = []
    sorted_results = sorted(results, key=sort_by_count, reverse=True)
    return sorted_results
