# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
from mlab_api.data.table_config import get_table_config
from mlab_api.constants import TABLE_KEYS
from mlab_api.data.base_data import Data
import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du

class ClientAsnData(Data):
    '''
    Connect to BigTable and pull down data.
    '''

    def get_client_metrics(self, client_id, timebin, starttime, endtime):
        '''
        Get data for client location at a specific
        timebin between start and stop times.
        '''

        table_config = get_table_config(self.table_configs, timebin, TABLE_KEYS["clients"])

        location_key_fields = du.get_key_fields([client_id], table_config)
        formatted = bt.get_time_metric_results(location_key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "clients")

        # set the ID to be the location ID
        formatted["meta"]["id"] = client_id

        return formatted


    def get_client_server_metrics(self, client_id, server_id, timebin, starttime, endtime):
        '''
        Get data for a specific client + server at a
        timebin between start and stop times.
        '''

        agg_name = TABLE_KEYS["servers"] + '_' + TABLE_KEYS["clients"]

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        location_key_fields = du.get_key_fields([server_id, client_id], table_config)
        formatted = bt.get_time_metric_results(location_key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "clients")

        # set the ID to be the location ID
        formatted["meta"]["id"] = client_id

        return formatted
