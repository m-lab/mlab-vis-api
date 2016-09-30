# -*- coding: utf-8 -*-
'''
Base Data Class
'''

import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du
from mlab_api.data.table_config import get_table_config

class Data(object):
    '''
    Connect to BigTable and pull down data.
    '''

    def __init__(self, table_configs, connection_pool):
        '''
        Constructor.
        '''
        self.connection_pool = connection_pool
        self.table_configs = table_configs


    def get_pool(self):
        '''
        Return Bigtable connection pool
        '''
        return self.connection_pool

    def get_list_data(self, entity_id, entity_type, query_type, include_data):
        '''
        Helper method to get out data from a list table.

        entity_id = id of entity to look for
        entity_type = [locations, clients, servers]
        query_type = [locations, clients, servers]  - what we are faceting on
        include_data = boolean to indicate if data should be queried and returned.
        '''

        config_id = du.list_table(query_type, entity_type)

        metric_name = "_".join([entity_type, query_type])

        table_config = get_table_config(self.table_configs, None, config_id)

        key_fields = du.get_key_fields([entity_id], table_config)

        results = bt.get_list_table_results(key_fields, self.get_pool(), include_data, table_config, metric_name)
        return {"results": results}
