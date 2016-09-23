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
    'locations': []
}


class SearchData(Data):

    def get_table_name(self, search_type, search_filter):
        if search_filter['type']:
            # its a list table we want
            return du.list_table(search_type, search_filter['type'])
        else:
            # its a search table we want
            return du.search_table(search_type)


    def filter_results(self, search_type, results, search_query):
        result_keys = SEARCH_KEYS[search_type]
        filtered_results = []
        for row in results:
            for result_key in result_keys:
                if result_key in row['meta']:
                    print(row['meta'][result_key])
                    if search_query in normalize_key(row['meta'][result_key]):
                        filtered_results.append(row)
                else:
                    print row
        return filtered_results


    def get_filtered_search_results(self, search_type, search_query, search_filter):
        if not search_filter['type'] or search_filter['type'] == search_type:
            return []
        table_name = self.get_table_name(search_type, search_filter)

        table_config = get_table_config(self.table_configs,
                                        None,
                                        table_name)

        union_results = []
        for filter_value in search_filter['value']:
            # we always want this filter value to be the first key
            key_prefix = du.get_key_field(filter_value, 0, table_config)
            key_prefix += du.BIGTABLE_KEY_DELIM
            tablefilter = FamilyNameRegexFilter('meta')
            results = bt.scan_table(table_config, self.get_pool(), prefix=key_prefix, filter=tablefilter)
            filtered_results = self.filter_results(search_type, results, search_query)
            union_results += filtered_results
        return union_results


    def get_basic_search_results(self, search_type, search_query):
        table_name = du.search_table(search_type)
        table_config = get_table_config(self.table_configs,
                                        None,
                                        table_name)

        results = bt.scan_table(table_config, self.get_pool(), prefix=search_query)
        return results


    def get_search_results(self, search_type, search_query, search_filter):
        results = []
        if search_filter['type']:
            results = self.get_filtered_search_results(search_type, search_query, search_filter)
        else:
            results = self.get_basic_search_results(search_type, search_query)

        # sort based on test_count
        if len(results) > 0 and 'data' in results:
            sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
            return {"results": sorted_results}
        else:
            return {"results": results}
