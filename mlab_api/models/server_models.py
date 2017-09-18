# -*- coding: utf-8 -*-
'''
Models for definging return value of Server specific calls
'''

from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.format_utils import meta_results_to_csv, \
    meta_data_in_row_to_csv, meta_data_to_csv

from mlab_api.models.base_models import SEARCH_DATA_FIELDS, \
    METRIC_META_FIELDS, SERVER_SEARCH_META_FIELDS, SERVER_META_FIELDS

# -------------------------------------------
# Servers: search
# -------------------------------------------
SERVER_SEARCH_RESULTS_FIELD = api.model('Server ASN Search Result', {
    'meta': fields.Nested(SERVER_SEARCH_META_FIELDS, required=True),
    'data': fields.Nested(SEARCH_DATA_FIELDS, required=True)
})

SERVER_SEARCH_MODEL = api.model('Server ASN Search Results', {
    'results': fields.List(fields.Nested(SERVER_SEARCH_RESULTS_FIELD),
                           required=True)
})


def server_search_to_csv(data):
    '''
    Converts server search results into a CSV
    '''
    return meta_data_in_row_to_csv(data, SERVER_SEARCH_META_FIELDS,
                                   SEARCH_DATA_FIELDS)


# -------------------------------------------
# Servers: info
# -------------------------------------------
SERVER_INFO_MODEL = api.model('Server Info Model', {
    'meta': fields.Nested(SERVER_SEARCH_META_FIELDS, required=True),
})

def server_info_to_csv(data):
    '''
    Converts server info to csv format
    '''
    return meta_data_to_csv(data, SERVER_META_FIELDS, None)


# -------------------------------------------
# Servers: metrics
# -------------------------------------------
SERVER_METRIC_MODEL = api.model('Server Metric Model', {
    'meta': fields.Nested(SERVER_META_FIELDS, required=True),
    'results': fields.List(fields.Nested(METRIC_META_FIELDS), required=True)
})

def server_metric_to_csv(data):
    '''
    Converts server metric data to CSV
    '''
    return meta_results_to_csv(data, SERVER_META_FIELDS, METRIC_META_FIELDS)
