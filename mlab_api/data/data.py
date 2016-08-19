# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
import logging

from mlab_api.data.table_config import get_table_config
import mlab_api.data.data_utils as du
# from gcloud.bigtable.row_filters import FamilyNameRegexFilter

CLIENT_LOCATION_KEY = 'client_loc'
CLIENT_ASN_KEY = 'client_asn'

class Data(object):
    '''
    Connect to BigTable and pull down data.
    '''

    def __init__(self, app_config, table_configs):
        '''
        Constructor.
        '''
        self.connection_pool = du.init_pool(app_config)
        self.table_configs = table_configs


    def get_pool(self):
        return self.connection_pool

    def scan_table(self, table_config, prefix="", start_key="", end_key="",  **kwargs):
        table_id = table_config['bigtable_table_name']

        # build table query parameters.
        # if prefix is present, use that.
        # else, use start / end key
        params = {}
        if len(prefix) > 0:
            params = {"row_prefix": prefix.encode('utf-8')}
        else:
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
                with self.get_pool().connection(timeout=5) as connection:
                    connection.open()
                    table = connection.table(table_id)

                    for _, data in table.scan(**params):
                        results.append(du.parse_row(data, table_config.columns))
            except Exception as err:
            # TODO: use specific exception catch.
                logging.warning("Failed query attempt %s", str(attempt))
                logging.warning(err)
            else:
                break
        else:
            results = []
        return results

    def get_row(self, table_config, row_key,  **kwargs):
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
                with self.get_pool().connection(timeout=5) as connection:
                    connection.open()
                    table = connection.table(table_id)

                    data = table.row(row_key, **kwargs)
                    row = du.parse_row(data, table_config.columns)
            except Exception as err:
            # TODO: use specific exception catch.
                logging.warning("Failed query attempt %s", str(attempt))
                logging.warning(err)
            else:
                break
        else:
            row = {}
        return row


    def get_location_info(self, location_id):
        '''
        Get info about specific location
        '''

        table_config = get_table_config(self.table_configs,
                                        None,
                                        CLIENT_LOCATION_KEY + '_list')
        location_key_fields = du.get_location_key_fields(location_id, table_config)

        row_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields)
        row = self.get_row(table_config, row_key)
        return row

    def get_location_metrics(self, location_id, time_aggregation, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.
        '''

        table_config = get_table_config(self.table_configs,
                                        time_aggregation,
                                        CLIENT_LOCATION_KEY)


        location_key_fields = du.get_location_key_fields(location_id, table_config)

        starttime_fields = du.get_time_key_fields(starttime, time_aggregation, table_config)
        endtime_fields = du.get_time_key_fields(endtime, time_aggregation, table_config)

        start_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields + starttime_fields)
        end_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields + endtime_fields)

        # BIGTABLE QUERY
        results = self.scan_table(table_config, start_key=start_key, end_key=end_key)

        return du.format_metric_data(results)

    def get_location_client_isps(self, location_id):
        '''
        Get list and info of client isps for a location
        '''

        config_id = CLIENT_LOCATION_KEY + '_' + CLIENT_ASN_KEY + '_list'

        table_config = get_table_config(self.table_configs, None, config_id)

        location_key_fields = du.get_location_key_fields(location_id, table_config)

        location_key_field = du.BIGTABLE_KEY_DELIM.join(location_key_fields)

        # results = self.scan_table(table_config, prefix=location_key_field, limit=1000, filter=FamilyNameRegexFilter('meta'))
        results = self.scan_table(table_config, prefix=location_key_field, limit=1000)
        return {"results": results}

    def get_location_client_isp_info(self, location_id, client_isp_id):
        '''
        Get static information about
        '''

        config_id = CLIENT_LOCATION_KEY + '_' + CLIENT_ASN_KEY + '_list'
        table_config = get_table_config(self.table_configs, None, config_id)

        key_fields = du.get_key_fields([location_id, client_isp_id], table_config)

        row_key = du.BIGTABLE_KEY_DELIM.join(key_fields)

        results = self.get_row(table_config, row_key)
        return results



    def get_location_client_isp_metrics(self, location_id, client_isp_id,
                                        time_aggregation, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times for a
        specific client ISP.
        '''
        # Create Row Key
        agg_name = CLIENT_ASN_KEY + '_' + CLIENT_LOCATION_KEY

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

        results = self.scan_table(table_config, start_key=start_key, end_key=end_key)

        # format output for API
        return du.format_metric_data(results)

    def get_location_search(self, location_query):
        '''
        API for location search
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        CLIENT_LOCATION_KEY + '_search')


        results = self.scan_table(table_config, prefix=location_query)

        # sort based on test_count
        sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
        return {"results": sorted_results}


    def get_location_children(self, location_id, type_filter=None):
        '''
        Return information about children regions of a location
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        CLIENT_LOCATION_KEY + '_list')
        location_key_fields = du.get_location_key_fields(location_id, table_config)

        location_key_field = du.BIGTABLE_KEY_DELIM.join(location_key_fields)

        results = self.scan_table(table_config, prefix=location_key_field)
        if type_filter:
            results = [r for r in results if r['meta']['type'] == type_filter]

        return {"results": results}


    # ----
    # ASN Data methods
    # ----
    # TODO: breakup data methods.

    def get_asn_search(self, asn_query):
        '''
        API for location search
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        'asn_search')

        results = self.scan_table(table_config, prefix=asn_query)

        # sort based on test_count
        sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
        return {"results": sorted_results}
