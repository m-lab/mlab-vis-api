# -*- coding: utf-8 -*-
'''
Test whether BigTable connection works
'''
import os
from mlab_api.data.bigtable_utils import init_pool, scan_table
from mlab_api.data.table_config import get_table_config, read_table_configs
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
  os.path.abspath('../mlab-keys/mlab-viz-bigtable-production@mlab-oti.iam.gserviceaccount.com-creds.json')
)

# credentials = GoogleCredentials.get_application_default()
print 'Using credentials' + credentials.service_account_email


os.environ['PROJECT'] = "mlab-oti"
os.environ['BIGTABLE_INSTANCE'] = "mlab-data-viz-prod"
os.environ['BIGTABLE_POOL_SIZE'] = "1"
os.environ['BIGTABLE_CONFIG_DIR'] = "bigtable_configs"

print 'Environment variables'
print os.environ

print 'Connect to db'
pool = init_pool()
table_configs = read_table_configs("bigtable_configs")
table_name = 'client_loc_search'
table_config = get_table_config(table_configs, None, table_name)

print 'Query db'
results = scan_table(table_config, pool, limit=3)

print 'Results'
print results
