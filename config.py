'''
Configurations for Flask App
'''

DEBUG = True
GOOGLE_PROJECT_ID = 'mlab-oti'
BIGTABLE_INSTANCE = 'mlab-ndt-agg'

# BIGTABLE_CONFIG_DIR = '../pipeline/dataflow/data/bigtable'
BIGTABLE_CONFIG_DIR = 'bigtable_configs'

DEFAULT_TIME_WINDOWS = {
    'day': {'starttime': '2015-10-01', 'endtime': '2015-10-31'},
    'month': {'starttime': '2015-01', 'endtime': '2015-12'},
    'year': {'starttime': '2010', 'endtime': '2015'},
    'day_hour': {'starttime': '2015-10-01+0', 'endtime': '2015-10-31+23'},
    'month_hour': {'starttime': '2015-01', 'endtime': '2015-10'}
}
