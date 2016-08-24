# -*- coding: utf-8 -*-
'''
Data instances to use in endpoints
'''

from mlab_api.app import app
from mlab_api.data.location_data import LocationData
from mlab_api.data.asn_data import AsnData
from mlab_api.data.table_config import read_table_configs
from mlab_api.data.bigtable_utils import init_pool

TABLE_CONFIGS = read_table_configs(app.config['BIGTABLE_CONFIG_DIR'])
pool = init_pool(app.config)

LOCATION_DATA = LocationData(TABLE_CONFIGS, pool)
ASN_DATA = AsnData(TABLE_CONFIGS, pool)
