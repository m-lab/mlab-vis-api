# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
from mlab_api.data.table_config import get_table_config
from mlab_api.data.base_data import Data, CONSTS
import mlab_api.data.bigtable_utils as bt

class ServerAsnData(Data):
    '''
    Connect to BigTable and pull down data.
    '''

    def get_server_asn_search(self, asn_query):
        '''
        API for location search
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        CONSTS["SERVER_ASN_KEY"] + "_search")

        results = bt.scan_table(table_config, self.get_pool(), prefix=asn_query)

        # sort based on test_count
        sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
        return {"results": sorted_results}

    def get_server_asn_metrics(self, asn_id, time_aggregation, startdate, enddate):
        return {"results": []}
