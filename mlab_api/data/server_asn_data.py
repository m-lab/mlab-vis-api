# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
# from mlab_api.data.table_config import get_table_config
from mlab_api.data.base_data import Data
# import mlab_api.data.bigtable_utils as bt
# import mlab_api.data.data_utils as du

class ServerAsnData(Data):
    '''
    Connect to BigTable and pull down data.
    '''

    def get_server_asn_metrics(self, asn_id, time_aggregation, startdate, enddate):
        return {"results": []}
