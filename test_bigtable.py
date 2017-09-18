# -*- coding: utf-8 -*-
'''
Test whether BigTable connection works
'''
import os
from mlab_api.data.bigtable_utils import init_pool, scan_table
from mlab_api.data.table_config import get_table_config, read_table_configs
from google.oauth2 import service_account

CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.abspath(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
)

# credentials = GoogleCredentials.get_application_default()
print 'Using credentials' + CREDENTIALS.service_account_email

print 'Environment variables'
print os.environ

print 'Connect to db'
POOL = init_pool()
TABLE_CONFIGS = read_table_configs("bigtable_configs")
TABLE_NAME = 'client_loc_search'
TABLE_CONFIG = get_table_config(TABLE_CONFIGS, None, TABLE_NAME)

print 'Query db'
RESULTS = scan_table(TABLE_CONFIG, POOL, limit=3)

print 'Results'
print RESULTS
