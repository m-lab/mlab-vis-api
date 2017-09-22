# -*- coding: utf-8 -*-
'''
Models for locations
'''
from flask_restplus import fields
from mlab_api.rest_api import API
from mlab_api.format_utils import meta_results_to_csv, meta_data_to_csv, \
    meta_data_in_row_to_csv, meta_in_row_to_csv

from mlab_api.models.base_models import LOCATION_META_FIELDS, \
    METRIC_META_FIELDS, LOCATION_CLIENT_META_FIELDS, \
    LOCATION_CLIENT_SERVER_META_FIELDS, LOCATION_SEARCH_META_FIELDS, \
    SEARCH_DATA_FIELDS, LOCATION_INFO_DATA_FIELDS, LOCATION_SERVER_META_FIELDS


# -------------------------------------------
# Locations: search
# -------------------------------------------
LOCATION_SEARCH_RESULT_FIELDS = API.model('Search Result', {
    'meta': fields.Nested(LOCATION_SEARCH_META_FIELDS, required=True),
    'data': fields.Nested(SEARCH_DATA_FIELDS, required=False)
})

LOCATION_SEARCH_MODEL = API.model('Location Search Model', {
    'results': fields.List(fields.Nested(LOCATION_SEARCH_RESULT_FIELDS),
                           required=True)
})

def location_search_to_csv(data):
    '''
    Convert location search results to CSV
    '''
    return meta_data_in_row_to_csv(data, LOCATION_SEARCH_META_FIELDS,
                                   SEARCH_DATA_FIELDS)


# ------------------------------------------------------
# Location + Client: list
# ------------------------------------------------------
LOCATION_CLIENT_LIST_MODEL = API.model('Location Client List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(LOCATION_CLIENT_META_FIELDS, required=True)
    }))
})

def location_client_list_to_csv(data):
    '''
    Convert location client list to CSV
    '''
    return meta_in_row_to_csv(data, LOCATION_CLIENT_META_FIELDS)


# ------------------------------------------------------
# Location + Server: list
# ------------------------------------------------------
LOCATION_SERVER_LIST_MODEL = API.model('Location Server List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(LOCATION_SERVER_META_FIELDS, required=True)
    }))
})

def location_server_list_to_csv(data):
    '''
    Convert location server list to CSV
    '''
    return meta_in_row_to_csv(data, LOCATION_SERVER_META_FIELDS)


# -------------------------------------------
# Location: info
# -------------------------------------------
LOCATION_INFO_MODEL = API.model('Location Info Model', {
    'meta': fields.Nested(LOCATION_META_FIELDS, required=True),
    'data': fields.Nested(LOCATION_INFO_DATA_FIELDS, required=True),
})

def location_info_to_csv(data):
    '''
    Convert location information to CSV
    '''
    return meta_data_to_csv(data, LOCATION_META_FIELDS,
                            LOCATION_INFO_DATA_FIELDS)

# -------------------------------------------
# Location: children info
# -------------------------------------------
LOCATION_CHILDREN_MODEL = API.model('Location Children Info Model', {
    "results": fields.List(fields.Nested(LOCATION_INFO_MODEL))
})

def location_children_to_csv(data):
    '''
    Convert location children data to CSV
    '''
    return meta_data_in_row_to_csv(data, LOCATION_META_FIELDS,
                                   LOCATION_INFO_DATA_FIELDS)


# ------------------------------------------------------
# Location + Client: info
# ------------------------------------------------------
LOCATION_CLIENT_ISP_INFO_MODEL = API.model('Location Client ASN Model', {
    'meta': fields.Nested(LOCATION_CLIENT_META_FIELDS, required=True),
    'data': fields.Nested(LOCATION_INFO_DATA_FIELDS, required=True)
})

def location_client_isp_info_to_csv(data):
    '''
    Convert location client ISP information to CSV
    '''
    return meta_data_to_csv(data, LOCATION_CLIENT_META_FIELDS,
                            LOCATION_INFO_DATA_FIELDS)


# -------------------------------------------
# Locations: metrics
# -------------------------------------------
LOCATION_METRIC_MODEL = API.model('Location Metric Model', {
    'meta': fields.Nested(LOCATION_META_FIELDS, required=True),
    'results': fields.List(fields.Nested(METRIC_META_FIELDS), required=True)
})

def location_metric_to_csv(data):
    '''
    Convert location metric to CSV
    '''
    return meta_results_to_csv(data, LOCATION_META_FIELDS, METRIC_META_FIELDS)

# -------------------------------------------
# Location + Clients: metrics
# -------------------------------------------
LOCATION_CLIENT_METRIC_MODEL = API.model('Location+Client Metric Model', {
    'meta': fields.Nested(LOCATION_CLIENT_META_FIELDS, required=True),
    'results': fields.List(fields.Nested(METRIC_META_FIELDS), required=True)
})

def location_client_metric_to_csv(data):
    '''
    Convert location client metrics to CSV
    '''
    return meta_results_to_csv(data, LOCATION_CLIENT_META_FIELDS,
                               METRIC_META_FIELDS)


# -------------------------------------------
# Location + Server: metrics
# -------------------------------------------
LOCATION_SERVER_METRIC_MODEL = API.model('Location+Server Metric Model', {
    'meta': fields.Nested(LOCATION_SERVER_META_FIELDS, required=True),
    'results': fields.List(fields.Nested(METRIC_META_FIELDS), required=True)
})

def location_server_metric_to_csv(data):
    '''
    Convert server metrics model to CSV
    '''
    return meta_results_to_csv(data, LOCATION_SERVER_META_FIELDS,
                               METRIC_META_FIELDS)


# -------------------------------------------
# Location + Client + Server: metrics
# -------------------------------------------
LOCATION_CLIENT_SERVER_METRIC_MODEL = API.model(
    'Location+Client+Server Metric Model', {
        'meta': fields.Nested(LOCATION_CLIENT_SERVER_META_FIELDS,
                              required=True),
        'results': fields.List(fields.Nested(METRIC_META_FIELDS),
                               required=True)
    })

def location_client_server_metric_to_csv(data):
    '''
    Convert location client and server metrics to CSV
    '''
    return meta_results_to_csv(data, LOCATION_CLIENT_SERVER_META_FIELDS,
                               METRIC_META_FIELDS)
