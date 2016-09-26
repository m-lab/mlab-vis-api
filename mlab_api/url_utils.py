# -*- coding: utf-8 -*-
'''
Utilities for working with URL inputs
'''

import re

def get_time_window(args, defaults):
    '''
    Returns starttime and endtime specified by args.
    If no value supplied, finds default value from defaults
    '''
    timebin = args.get('timebin')
    startdate = args.get('startdate')
    if (not startdate) and (timebin in defaults):
        startdate = defaults[timebin]['startdate']

    enddate = args.get('enddate')
    if (not enddate) and (timebin in defaults):
        enddate = defaults[timebin]['enddate']

    return (startdate, enddate)

def normalize_key(location_key):
    '''
    Provides consistent search strings
    '''
    return re.sub('[\W|_]', '', location_key.lower())

def get_filter(args):
    ftype = args.get('filtertype')
    fvalue = args.get('filtervalue')

    if( ftype and fvalue):
        fvalues = fvalue.split(",")
        return {'type': ftype, 'value':fvalues}
    return {'type': None, 'value': []}
