# -*- coding: utf-8 -*-
'''
Data class for accessing data for search
'''
from google.cloud.bigtable.row_filters import FamilyNameRegexFilter
from mlab_api.data.table_config import get_table_config
from mlab_api.data.base_data import Data
from mlab_api.url_utils import normalize_key
from mlab_api.sort_utils import sort_by_count
import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du

SEARCH_KEYS = {
    'servers': ['server_asn_name'],
    'clients': ['client_asn_name'],
    'locations': ['client_continent', 'client_country', 'client_region', 'client_city']
}

DATA_VALUES = ['test_count', 'last_three_month_test_count', 'last_year_test_count']


class SearchData(Data):

    def get_row_search_key(self, row, result_keys):
        '''
        Returns search key for provided row.
        Search key is based on provided result_keys array.
        '''
        row_keys = [row['meta'][key] for key in result_keys if key in row['meta']]
        return normalize_key(''.join(row_keys))

    def get_table_name(self, search_type, search_filter):
        '''
        Returns name of table for provided search type.

        search_type = type of search.
        search_filter = optional filter we are searching within.
        '''
        if search_filter['type']:
            # its a list table we want
            return du.list_table(search_type, search_filter['type'])
        else:
            # its a search table we want
            return du.search_table(search_type)

    def merge_rows(self, row, prev_row):
        '''
        Takes 2 rows and merges values from DATA_VALUES
        '''
        for key in DATA_VALUES:
            if (key in prev_row['meta']) and (key in row['meta']):
                prev_row['meta'][key] += row['meta'][key]
        return prev_row

    def filter_results(self, search_type, search_query, results):
        '''
        Given a list of results and a query, filter matching results.

        search_type: one of ['locations', 'servers', 'clients']
        search_query: input query from api
        results: raw unfiltered results
        included_keys: list of existing keys already in the total results.
        '''

        # result_keys are the keys to search in the result rows for
        # the `search_query`
        merged_results = {}
        result_keys = SEARCH_KEYS[search_type]
        for row in results:
            # if result_keys is > 1, provides a merged string to search in
            row_key = self.get_row_search_key(row, result_keys)
            # only add if not already in the results.
            if ((search_query is None) or (search_query in row_key)):
                if (row_key not in merged_results):
                    merged_results[row_key] = row
                else:
                    # attempt to add count values togehter.
                    new_row = self.merge_rows(row, merged_results[row_key])
                    merged_results[row_key] = new_row
        return merged_results.values()

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


    def get_filtered_search_results(self, search_type, search_query, search_filter, **kwargs):
        '''
        Filter search. Provides results for searches that are faceted.

        search_type = one of ['locations', 'servers', 'clients']
        search_query = input query from api
        search_filter = {type: ['locations', 'servers', 'clients'], value:[id1, id2]}
        '''
        if not search_filter['type'] or search_filter['type'] == search_type:
            return []
        table_name = self.get_table_name(search_type, search_filter)

        table_config = get_table_config(self.table_configs, None, table_name)

        all_results = []
        for filter_value in sorted(search_filter['value'], reverse=False):
            # we always want this filter value to be the first key
            key_prefix = du.get_key_field(filter_value, 0, table_config)
            key_prefix += du.BIGTABLE_KEY_DELIM
            # filter only the `meta` column family - for speed.
            tablefilter = FamilyNameRegexFilter('meta')
            all_results += bt.scan_table(table_config, self.get_pool(), prefix=key_prefix, filter=tablefilter, **kwargs)

        filtered_results = self.filter_results(search_type, search_query, all_results)

        return self.prepare_filtered_search_results(filtered_results)


    def get_basic_search_results(self, search_type, search_query):
        '''
        Provide basic search with no filtering logic.
        Basic search is based purely on bigtable prefix scans.
        '''
        table_name = du.search_table(search_type)
        table_config = get_table_config(self.table_configs, None, table_name)

        results = bt.scan_table(table_config, self.get_pool(), prefix=search_query)
        return results


    def get_search_results(self, search_type, search_query, search_filter):
        '''
        Root search method. calls into basic search or filtered search depending on
        specific search parameters.

        search_type = type of search being performed.
        search_query = query key of search
        search_filter = filter to search within.
        '''
        results = []
        if search_filter['type']:
            results = self.get_filtered_search_results(search_type, search_query, search_filter)
        else:
            results = self.get_basic_search_results(search_type, search_query)

        # sort based on test_count
        if len(results) > 0 and 'meta' in results[0]:
            sorted_results = sorted(results, key=sort_by_count, reverse=True)
            return {"results": sorted_results}
        else:
            return {"results": results}

    def get_top_results(self, search_type, top_n, search_filter):
        '''
        Use same logic as filtered search to get top N filtered results.

        search_type = type of search being performed.
        top_n = integer max count to return
        search_filter = filter to search within.
        '''

        # limit here to prevent bigtable queries from timing out.
        results = self.get_filtered_search_results(search_type, None, search_filter, limit=300)
        if not top_n:
            top_n = -1

        sorted_results = []
        if len(results) > 0 and 'meta' in results[0]:
            sorted_results = sorted(results, key=sort_by_count, reverse=True)
        return {"results": sorted_results[0:top_n]}
