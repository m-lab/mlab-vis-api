# -*- coding: utf-8 -*-
'''
Data class for accessing data for search
'''
from gcloud.bigtable.row_filters import FamilyNameRegexFilter
from mlab_api.data.table_config import get_table_config
from mlab_api.data.base_data import Data
from mlab_api.url_utils import normalize_key
import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du

SEARCH_KEYS = {
    'servers': ['server_asn_name'],
    'clients': ['client_asn_name'],
    'locations': ['client_continent', 'client_country', 'client_region', 'client_city']
}


class SearchData(Data):

    def get_row_search_key(self, row, result_keys):
        row_keys = [row['meta'][key] for key in result_keys if key in row['meta']]
        return normalize_key(''.join(row_keys))

    def get_table_name(self, search_type, search_filter):
        if search_filter['type']:
            # its a list table we want
            return du.list_table(search_type, search_filter['type'])
        else:
            # its a search table we want
            return du.search_table(search_type)


    def filter_results(self, search_type, results, search_query, result_keys):
        result_keys = SEARCH_KEYS[search_type]
        filtered_results = []
        for row in results:
            row_key = self.get_row_search_key(row, result_keys)
            if (row_key not in result_keys) and (search_query in row_key):
                filtered_results.append(row)
                result_keys.append(row_key)
        return filtered_results


    def get_filtered_search_results(self, search_type, search_query, search_filter):
        '''
        filter search
        '''
        if not search_filter['type'] or search_filter['type'] == search_type:
            return []
        table_name = self.get_table_name(search_type, search_filter)

        table_config = get_table_config(self.table_configs,
                                        None,
                                        table_name)

        union_results = []
        result_keys = []
        for filter_value in search_filter['value']:
            # we always want this filter value to be the first key
            key_prefix = du.get_key_field(filter_value, 0, table_config)
            key_prefix += du.BIGTABLE_KEY_DELIM
            tablefilter = FamilyNameRegexFilter('meta')
            results = bt.scan_table(table_config, self.get_pool(), prefix=key_prefix, filter=tablefilter)
            filtered_results = self.filter_results(search_type, results, search_query, result_keys)
            union_results += filtered_results
        return union_results


    def get_basic_search_results(self, search_type, search_query):
        '''
        basic search
        '''
        table_name = du.search_table(search_type)
        table_config = get_table_config(self.table_configs,
                                        None,
                                        table_name)

        results = bt.scan_table(table_config, self.get_pool(), prefix=search_query)
        return results


    def get_search_results(self, search_type, search_query, search_filter):
        '''
        Root method
        '''
        results = []
        if search_filter['type']:
            results = self.get_filtered_search_results(search_type, search_query, search_filter)
        else:
            results = self.get_basic_search_results(search_type, search_query)

        # sort based on test_count
        if len(results) > 0 and 'data' in results:
            sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
            return {"results": sorted_results}
        # elif len(results) > 0 and 'meta' in results:
        #     sorted_results = sorted(results, key=lambda k: k['meta']['test_count'], reverse=True)
        #     return {"results": sorted_results}
        else:
            return {"results": results}
