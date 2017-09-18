# -*- coding: utf-8 -*-
'''
Shared ASN functions between client and server classes.
'''
#pylint: disable=no-name-in-module
from google.cloud.bigtable.row_filters import FamilyNameRegexFilter

import mlab_api.data.bigtable_utils as bt
import mlab_api.data.data_utils as du

def get_bt_results(key_fields, table_config, pool):
    '''
    Scans for and returns big table results based on key fields
    and a table config

    key_fields = key fields for the search
    table_config = the table to scan
    pool = a big table connection pool

    '''
    prefix_key = du.BIGTABLE_KEY_DELIM.join(key_fields)
    results = bt.scan_table(table_config, pool, prefix=prefix_key, limit=1,
                            filter=FamilyNameRegexFilter('meta'))

    result = {}

    if results:
        result = results[0]

    return result
