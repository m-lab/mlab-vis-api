# -*- coding: utf-8 -*-
'''
Module for handling table configuration objects
'''
from __future__ import print_function
import glob
import os
from mlab_api.os_utils import read_json

class TableConfig(object):
    '''
    Class to represent a single table config object
    '''

    def __init__(self, config):
        '''
        Create a table configuration based on a dictionary
        '''
        self.config = config

        # store the key
        self.key = make_config_key(
            config['frequency'] if 'frequency' in config else None,
            config['key'])

        # create the column configs object
        self.columns = get_column_configs(config)
        self.keys = get_keys_configs(config)

    def __getitem__(self, key):
        '''
        Implement [] operator
        '''
        return self.config[key]

    def __contains__(self, key):
        '''
        Implement in operator
        '''
        return key in self.config

    def __str__(self):
        '''
        Print representation
        '''
        return str(self.config)

def read_table_configs(config_dir):
    '''
    Reads in a collection of bigtable configs based on the BIGTABLE_CONFIG_DIR
    and returns them as a keyed list, mapping key to TableConfig object
    '''

    configs = None
    if config_dir:
        configs = read_configs(config_dir)
    else:
        print('WARNING: no BIGTABLE_CONFIG_DIR provided')
        configs = {}

    return configs

def read_configs(config_directory):
    '''
    Read a set of bigtable config files from a directory
    '''
    configs = {}
    config_filenames = glob.glob(os.path.join(os.getcwd(), config_directory,
                                              "*.json"))
    print(os.path.join(os.getcwd(), config_directory, "*.json"))
    for config_filename in config_filenames:
        config = TableConfig(read_json(config_filename))
        configs[config.key] = config

    return configs

def get_table_config(configs, time_aggregation, location_type):
    '''
    Pull out a particular table config from a dict of configs.
    '''
    return configs[make_config_key(time_aggregation, location_type)]


def make_config_key(time_aggregation, key_name):
    '''
    mash up frequency and key name to a config key
    '''
    if time_aggregation:
        return time_aggregation + "-" + key_name
    else:
        return key_name

def get_column_configs(config):
    '''
    Gets column configs
    '''

    col_configs = {}
    for col in config['columns']:
        col_configs[col['name']] = col
    return col_configs

def get_keys_configs(config):
    '''
    Gets keys configs
    '''

    key_configs = {}
    for key in config['row_keys']:
        key_configs[key['name']] = key
    return key_configs
