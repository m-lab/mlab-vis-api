# -*- coding: utf-8 -*-
'''
Data class for accessing data for raw data
'''
from mlab_api.data.table_config import get_table_config
from mlab_api.data.base_data import Data
from mlab_api.url_utils import normalize_key
from mlab_api.sort_utils import sort_by_count
import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du


class RawData(Data):
    '''
    Pull out some raw data
    '''

    def get_raw_test_results(self):
        '''
        Extract sample raw data.
        '''
        table_name = 'raw_sample'
        table_config = get_table_config(self.table_configs, None, table_name)
        results = bt.scan_table(table_config, self.get_pool(), limit=1000)
        return {"results": results}
