# -*- coding: utf-8 -*-
'''
OS (file-related) utils
'''
import json

def read_json(filename):
    '''
    Read a JSON file and return the dictionary representation of results
    '''
    data = {}
    with open(filename) as data_file:
        data = json.load(data_file)
    return data
