# -*- coding: utf-8 -*-
'''
Configurations for Flask App
'''
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

API_MODE = os.environ.get("API_MODE")
GOOGLE_PROJECT_ID = 'mlab-sandbox'
BIGTABLE_INSTANCE = 'mlab-data-viz'
BIGTABLE_POOL_SIZE = 40
GA_TRACKING_ID='UA-86118171-1'

# BIGTABLE_CONFIG_DIR = '../pipeline/dataflow/data/bigtable'
BIGTABLE_CONFIG_DIR = 'bigtable_configs'
