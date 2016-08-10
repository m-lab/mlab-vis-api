'''
Utilities for Testing
'''
import json

def read_json(filename):
    '''
    read json
    '''
    data = {}
    with open(filename) as data_file:
        data = json.load(data_file)
    return data
