'''
Test Table Config Module
'''
from mlab_api.data.table_config import TableConfig
from mlab_api.data.table_config import read_configs
from mlab_api.data.table_config import make_config_key
from mlab_api.data.table_config import get_column_configs

from utils import read_json


def test_read_configs():
    '''
    test read_configs
    '''
    config_dir = 'bigtable_configs'

    configs = read_configs(config_dir)
    assert len(configs.keys()) > 1

    first_key = configs.keys()[0]
    print first_key
    # grab the first config
    config = configs[first_key]

    # ensure it isn't empty
    assert 'bigtable_table_name' in config

    # ensure is a TableConfig
    assert isinstance(config, TableConfig)

    assert len(config.columns.keys()) > 1

def test_make_config_key():
    '''
    test make_config_key
    '''
    time = 'day'
    agg = 'client_city'

    key = make_config_key(time, agg)
    assert key == '-'.join([time, agg])

    key = make_config_key(None, agg)
    assert key == agg

def test_get_column_configs():
    '''
    test get_column_configs
    '''

    configfilename = 'bigtable_configs/client_loc_by_day.json'

    config_json = read_json(configfilename)

    columns = get_column_configs(config_json)
    assert len(columns.keys()) > 1

    assert 'count' in columns.keys()
