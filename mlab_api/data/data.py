'''
Data class for accessing data for API calls.
'''
from __future__ import print_function
import logging

from mlab_api.data.table_config import get_table_config
import mlab_api.data.data_utils as du

class Data(object):
    '''
    Connect to BigTable and pull down data.
    '''

    def __init__(self, app_config, table_configs):
        '''
        Constructor.
        '''
        self.connection = du.init_connection(app_config)
        self.table_configs = table_configs

    def get_connection(self):
        '''
        Returns current connection
        '''
        return self.connection

    def close(self):
        '''
        Close connection
        '''
        if self.connection:
            self.connection.close()


    def get_location_metrics(self, location_id, time_aggregation, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.
        '''

        location_type = du.get_location_type(location_id)

        table_config = get_table_config(self.table_configs,
                                        time_aggregation,
                                        location_type)


        location_key_fields = du.get_location_key_fields(location_id, table_config)

        starttime_fields = du.get_time_key_fields(starttime, time_aggregation, table_config)
        endtime_fields = du.get_time_key_fields(endtime, time_aggregation, table_config)

        start_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields + starttime_fields)
        end_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields + endtime_fields)

        table_id = table_config['bigtable_table_name']
        table = self.connection.table(table_id)

        logging.info("querying: %s", table_id)
        logging.info("start_key: %s", start_key)
        logging.info("end_key: %s", end_key)

        # HERE IS THE BIGTABLE QUERY
        # Note that we must encode utf-8 to handle unicode characters in location names
        results = []
        for _, data in table.scan(row_start=start_key.encode('utf-8'),
                                  row_stop=end_key.encode('utf-8')):
            results.append(du.parse_row(data, table_config.columns))
        return du.format_metrics(results)


    def get_location_client_isp_metrics(self, location_id, client_isp_id,
                                        time_aggregation, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times for a
        specific client ISP.

        TODO: currently only works for cities
        '''
        # Create Row Key
        location_type = du.get_location_type(location_id)
        agg_name = 'client_asn' + '_' + location_type

        table_config = get_table_config(self.table_configs,
                                        time_aggregation,
                                        agg_name)

        location_key_fields = du.get_location_key_fields(location_id, table_config)

        client_isp_fields = du.get_client_isp_fields(client_isp_id, table_config)

        starttime_fields = du.get_time_key_fields(starttime, time_aggregation, table_config)
        endtime_fields = du.get_time_key_fields(endtime, time_aggregation, table_config)

        # Start and End -- Row Keys
        start_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields +
                                               client_isp_fields +
                                               starttime_fields)

        end_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields +
                                             client_isp_fields +
                                             endtime_fields)

        # Prepare to query the table
        table_id = table_config['bigtable_table_name']
        table = self.connection.table(table_id)

        logging.info("querying: %s", table_id)
        logging.info("start_key: %s", start_key)
        logging.info("end_key: %s", end_key)


        # HERE IS THE BIGTABLE QUERY
        results = []
        for _, data in table.scan(row_start=start_key.encode('utf-8'),
                                  row_stop=end_key.encode('utf-8')):
            results.append(du.parse_row(data, table_config.columns))
        # format output for API
        return du.format_metrics(results)

    def get_location_search(self, location_query):
        '''
        API for location search
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        'client_location_search')

        table_id = table_config['bigtable_table_name']
        table = self.connection.table(table_id)

        logging.info("querying: %s", table_id)
        logging.info("prefex: %s", location_query)

        key_prefix = location_query

        # HERE IS THE BIGTABLE QUERY
        results = []
        for _, data in table.scan(row_prefix=key_prefix.encode('utf-8')):
            results.append(du.parse_row(data, table_config.columns))
        # sort based on test_count
        sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
        return {"results": sorted_results}
