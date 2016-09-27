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

DATA_VALUES = ['test_count', 'last_three_month_test_count', 'last_year_test_count']

def search_sort_key(row):
    if 'test_count' in row['meta']:
        return row['meta']['test_count']
    elif 'last_year_test_count' in row['meta']:
        return row['meta']['last_year_test_count']
    else:
        return 'a'

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


    def filter_results(self, search_type, search_query, results, included_keys):
        '''
        Given a list of results and a query, filter matching results.
        Also given a list of included keys, filter out duplicates
        search_type: one of ['locations', 'servers', 'clients']
        search_query: input query from api
        results: raw unfiltered results
        included_keys: list of existing keys already in the total results.
        '''

        # result_keys are the keys to search in the result rows for
        # the `search_query`
        result_keys = SEARCH_KEYS[search_type]
        filtered_results = []
        for row in results:
            # if result_keys is > 1, provides a merged string to search in
            row_key = self.get_row_search_key(row, result_keys)
            # only add if not already in the results.
            if (row_key not in included_keys) and (search_query in row_key):
                filtered_results.append(row)
                included_keys.append(row_key)
        return filtered_results

    def prepare_filtered_search_results(self, results):
        '''
        Augment raw results to make them ready for output.
        '''
        for row in results:
            if 'data' not in row:
                row['data'] = {}
            if 'meta' not in row:
                row['meta'] = {}
            for key in DATA_VALUES:
                if key in row['meta']:
                    row['data'][key] = row['meta'][key]

        return results



    def get_filtered_search_results(self, search_type, search_query, search_filter):
        '''
        Filter search. Provides results for searches that are faceted.
        search_type: one of ['locations', 'servers', 'clients']
        search_query: input query from api
        search_filter: {type: ['locations', 'servers', 'clients'], value:[id1, id2]}
        '''
        if not search_filter['type'] or search_filter['type'] == search_type:
            return []
        table_name = self.get_table_name(search_type, search_filter)

        table_config = get_table_config(self.table_configs,
                                        None,
                                        table_name)

        union_results = []
        included_keys = []
        for filter_value in search_filter['value']:
            # we always want this filter value to be the first key
            key_prefix = du.get_key_field(filter_value, 0, table_config)
            key_prefix += du.BIGTABLE_KEY_DELIM
            # filter only the `meta` column family - for speed.
            tablefilter = FamilyNameRegexFilter('meta')
            results = bt.scan_table(table_config, self.get_pool(), prefix=key_prefix, filter=tablefilter)
            filtered_results = self.filter_results(search_type, search_query, results, included_keys)
            union_results += filtered_results
        return self.prepare_filtered_search_results(union_results)


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

        print(results)

        # sort based on test_count
        if len(results) > 0 and 'meta' in results[0]:
            sorted_results = sorted(results, key=search_sort_key, reverse=True)
            return {"results": sorted_results}
        else:
            return {"results": results}
