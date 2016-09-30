# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
from gcloud.bigtable.row_filters import FamilyNameRegexFilter
from mlab_api.data.table_config import get_table_config
from mlab_api.constants import TABLE_KEYS
from mlab_api.data.base_data import Data
from mlab_api.decorators import add_ids, add_id
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

    @add_ids('client_asn_number')
    def get_server_clients(self, server_id, include_data):
        '''
        Get list and info of client isps for a server
        '''
        return self.get_list_data(server_id, 'servers', 'clients', include_data)


    @add_ids('location_key')
    def get_server_locations(self, server_id, include_data):
        '''
        Get list and info of locations for a server
        '''
        return self.get_list_data(server_id, 'servers', 'locations', include_data)


    @add_id('server_asn_number')
    def get_server_metrics(self, server_id, timebin, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.
        '''

        table_config = get_table_config(self.table_configs, timebin, TABLE_KEYS["servers"])

        location_key_fields = du.get_key_fields([server_id], table_config)
        formatted = bt.get_time_metric_results(location_key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "servers")


        return formatted
