# -*- coding: utf-8 -*-
'''
Models for definging return value of Client specific calls
'''

from flask_restplus import fields
from mlab_api.rest_api import API

from mlab_api.format_utils import meta_results_to_csv, meta_data_to_csv, \
    meta_data_in_row_to_csv, meta_in_row_to_csv

from mlab_api.models.base_models import SEARCH_DATA_FIELDS, \
    METRIC_META_FIELDS, CLIENT_SEARCH_META_FIELDS, CLIENT_META_FIELDS, \
    CLIENT_SERVER_META_FIELDS


# -------------------------------------------
# Clients: search
# -------------------------------------------
CLIENT_SEARCH_RESULT_FIELDS = API.model('Client ASN Search Result', {
    'meta': fields.Nested(CLIENT_SEARCH_META_FIELDS, required=True),
    'data': fields.Nested(SEARCH_DATA_FIELDS, required=True)
})

CLIENT_SEARCH_MODEL = API.model('Client ASN Search Results', {
    'results': fields.List(fields.Nested(CLIENT_SEARCH_RESULT_FIELDS),
                           required=True)

    })

def client_search_to_csv(data):
    '''
    Convert client search results to CSV
    '''
    return meta_data_in_row_to_csv(data, CLIENT_SEARCH_META_FIELDS,
                                   SEARCH_DATA_FIELDS)


# ------------------------------------------------------
# Client + Server List
# ------------------------------------------------------
CLIENT_SERVER_LIST_MODEL = API.model('Client Server List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(CLIENT_SERVER_META_FIELDS, required=True)
    }))
})

def client_server_list_to_csv(data):
    '''
    Convert client server list to CSV
    '''
    return meta_in_row_to_csv(data, CLIENT_SERVER_META_FIELDS)


# -------------------------------------------
# Clients: info
# -------------------------------------------
CLIENT_INFO_MODEL = API.model('Client Info Model', {
    'meta': fields.Nested(CLIENT_SEARCH_META_FIELDS, required=True),
})

def client_info_to_csv(data):
    '''
    Convert client info to CSV
    '''
    return meta_data_to_csv(data, CLIENT_META_FIELDS, None)

# -------------------------------------------
# Clients: metrics
# -------------------------------------------
CLIENT_METRIC_MODEL = API.model('Client Metric Model', {
    'meta': fields.Nested(CLIENT_META_FIELDS, required=True),
    'results': fields.List(fields.Nested(METRIC_META_FIELDS), required=True)
})

def client_metric_to_csv(data):
    '''
    Convert client metrics to CSV
    '''
    return meta_results_to_csv(data, CLIENT_META_FIELDS, METRIC_META_FIELDS)

# -------------------------------------------
# Clients + Servers: metrics
# -------------------------------------------
CLIENT_SERVER_METRIC_MODEL = API.model('Client+Server Metric Model', {
    'meta': fields.Nested(CLIENT_SERVER_META_FIELDS, required=True),
    'results': fields.List(fields.Nested(METRIC_META_FIELDS), required=True)
})

def client_server_metric_to_csv(data):
    '''
    Convert client server metric model to CSV
    '''
    return meta_results_to_csv(data, CLIENT_SERVER_META_FIELDS,
                               METRIC_META_FIELDS)
