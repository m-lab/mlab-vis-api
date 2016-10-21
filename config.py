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
GA_TRACKING_ID='UA-86118171-1'

# BIGTABLE_CONFIG_DIR = '../pipeline/dataflow/data/bigtable'
BIGTABLE_CONFIG_DIR = 'bigtable_configs'
