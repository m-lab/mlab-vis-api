# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
from gcloud.bigtable.row_filters import FamilyNameRegexFilter
from mlab_api.data.table_config import get_table_config
from mlab_api.constants import TABLE_KEYS
from mlab_api.data.base_data import Data
import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du

class ServerAsnData(Data):
    '''
    Connect to BigTable and pull down data.
    '''

    def get_server_info(self, server_id):
        '''
        Get info for a client
        '''

        # we are using a hack from list tables
        # so grab the first match from a list table faceted by server ids'
        table_name = du.list_table("clients", "servers")


        table_config = get_table_config(self.table_configs, None, table_name)


        key_fields = du.get_key_fields([server_id], table_config)
        prefix_key = du.BIGTABLE_KEY_DELIM.join(key_fields)
        results = bt.scan_table(table_config, self.get_pool(), prefix=prefix_key, limit=1, filter=FamilyNameRegexFilter('meta'))

        result = {}

        if len(results) > 0:
            result = results[0]

        return result

    def get_server_metrics(self, server_id, timebin, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.
        '''

        table_config = get_table_config(self.table_configs, timebin, TABLE_KEYS["servers"])

        location_key_fields = du.get_key_fields([server_id], table_config)
        formatted = bt.get_time_metric_results(location_key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "servers")

        # set the ID to be the location ID
        formatted["meta"]["id"] = server_id

        return formatted
