# -*- coding: utf-8 -*-
'''
Utilities for working with URL inputs
'''

import re

def get_time_window(args, time_aggregation, defaults):
    '''
    Returns starttime and endtime specified by args.
    If no value supplied, finds default value from defaults
    '''
    startdate = args.get('startdate')
    if (not startdate) and (time_aggregation in defaults):
        startdate = defaults[time_aggregation]['startdate']

    enddate = args.get('enddate')
    if (not enddate) and (time_aggregation in defaults):
        enddate = defaults[time_aggregation]['enddate']

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
        return {ftype: fvalue}
    return {}
