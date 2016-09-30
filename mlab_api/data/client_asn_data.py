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

class ClientAsnData(Data):
    '''
    Connect to BigTable and pull down data.
    '''

    def get_client_info(self, client_id):
        '''
        Get info for a client
        '''

        # we are using a hack from list tables
        # so grab the first match from a list table faceted by client ids'
        table_name = du.list_table("servers", "clients")


        table_config = get_table_config(self.table_configs, None, table_name)


        key_fields = du.get_key_fields([client_id], table_config)
        prefix_key = du.BIGTABLE_KEY_DELIM.join(key_fields)
        results = bt.scan_table(table_config, self.get_pool(), prefix=prefix_key, limit=1, filter=FamilyNameRegexFilter('meta'))

        result = {}

        if len(results) > 0:
            result = results[0]

        return result

    @add_ids('server_asn_number')
    def get_client_servers(self, client_id, include_data):
        '''
        Get list and info of server isps for a client
        '''

        return self.get_list_data(client_id, 'clients', 'servers', include_data)


    @add_ids('location_key')
    def get_client_locations(self, client_id, include_data):
        '''
        Get list and info of locations for a client
        '''

        return self.get_list_data(client_id, 'clients', 'locations', include_data)

    @add_id('client_asn_number')
    def get_client_metrics(self, client_id, timebin, starttime, endtime):
        '''
        Get data for client location at a specific
        timebin between start and stop times.
        '''

        table_config = get_table_config(self.table_configs, timebin, TABLE_KEYS["clients"])

        key_fields = du.get_key_fields([client_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "clients")

        return formatted


    @add_id(['client_asn_number', 'server_asn_number'])
    def get_client_server_metrics(self, client_id, server_id, timebin, starttime, endtime):
        '''
        Get data for a specific client + server at a
        timebin between start and stop times.
        '''

        agg_name = TABLE_KEYS["servers"] + '_' + TABLE_KEYS["clients"]

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        key_fields = du.get_key_fields([server_id, client_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "clients")

        return formatted
