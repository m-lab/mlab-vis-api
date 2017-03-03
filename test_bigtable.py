# -*- coding: utf-8 -*-
'''
Test whether BigTable connection works
'''
import os
from mlab_api.data.bigtable_utils import init_pool, scan_table
from mlab_api.data.table_config import get_table_config, read_table_configs
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
print 'Using credentials' + credentials.service_account_email

app_config = {
  'GOOGLE_PROJECT_ID': 'mlab-sandbox',
  'BIGTABLE_INSTANCE': 'mlab-data-viz',
  'BIGTABLE_POOL_SIZE': 1,
  'BIGTABLE_CONFIG_DIR': 'bigtable_configs'
}

print 'Environment variables'
print os.environ

print 'Connect to db'
pool = init_pool(app_config)
table_configs = read_table_configs(app_config['BIGTABLE_CONFIG_DIR'])
table_name = 'client_loc_search'
table_config = get_table_config(table_configs, None, table_name)

print 'Query db'
results = scan_table(table_config, pool, limit=3)

print 'Results'
print results