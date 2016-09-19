# -*- coding: utf-8 -*-
'''
Configurations for Flask App
'''
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

API_MODE = os.environ.get("API_MODE")
GOOGLE_PROJECT_ID = 'mlab-oti'
BIGTABLE_INSTANCE = 'mlab-ndt-agg'
BIGTABLE_POOL_SIZE = 40
STATSD_SERVER='104.155.133.245'

# BIGTABLE_CONFIG_DIR = '../pipeline/dataflow/data/bigtable'
BIGTABLE_CONFIG_DIR = 'bigtable_configs'

DEFAULT_TIME_WINDOWS = {
    'day': {'startdate': '2015-10-01', 'enddate': '2015-10-31'},
    'month': {'startdate': '2015-01', 'enddate': '2016-01'},
    'year': {'startdate': '2010', 'enddate': '2016'},
    'day_hour': {'startdate': '2015-10-01+0', 'enddate': '2015-11-01+0'},
    'month_hour': {'startdate': '2015-01', 'enddate': '2015-10'},
    'year_hour': {'startdate': '2015', 'enddate': '2016'}
}
