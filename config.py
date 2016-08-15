'''
Configurations for Flask App
'''

DEBUG = True
GOOGLE_PROJECT_ID = 'mlab-oti'
BIGTABLE_INSTANCE = 'mlab-ndt-agg'

# BIGTABLE_CONFIG_DIR = '../pipeline/dataflow/data/bigtable'
BIGTABLE_CONFIG_DIR = 'bigtable_configs'

DEFAULT_TIME_WINDOWS = {
    'day': {'startdate': '2015-10-01', 'enddate': '2015-10-31'},
    'month': {'startdate': '2015-01', 'enddate': '2016-01'},
    'year': {'startdate': '2010', 'enddate': '2016'},
    'day_hour': {'startdate': '2015-10-01+0', 'enddate': '2015-11-01+0'},
    'month_hour': {'startdate': '2015-01', 'enddate': '2015-10'}
}
