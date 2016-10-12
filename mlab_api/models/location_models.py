# -*- coding: utf-8 -*-
'''
Models for locations
'''
from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.format_utils import meta_results_to_csv, meta_data_to_csv, \
    meta_data_in_row_to_csv, meta_in_row_to_csv

from mlab_api.models.base_models import location_meta_fields, metric_data_fields, \
    location_client_meta_fields, location_client_server_meta_fields, \
    location_search_meta_fields, search_data_fields, location_info_data_fields, \
    location_server_meta_fields


# -------------------------------------------
# Locations: search
# -------------------------------------------
location_search_result_fields = api.model('Search Result', {
    'meta': fields.Nested(location_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=False)
})

location_search_model = api.model('Location Search Model', {
    'results': fields.List(fields.Nested(location_search_result_fields), required=True)
})

def location_search_to_csv(data):
    return meta_data_in_row_to_csv(data, location_search_meta_fields, search_data_fields)


# ------------------------------------------------------
# Location + Client: list
# ------------------------------------------------------
location_client_list_model = api.model('Location Client List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(location_client_meta_fields, required=True)
    }))
})

def location_client_list_to_csv(data):
    return meta_in_row_to_csv(data, location_client_meta_fields)


# ------------------------------------------------------
# Location + Server: list
# ------------------------------------------------------
location_server_list_model = api.model('Location Server List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(location_server_meta_fields, required=True)
    }))
})

def location_server_list_to_csv(data):
    return meta_in_row_to_csv(data, location_server_meta_fields)


# -------------------------------------------
# Location: info
# -------------------------------------------
location_info_model = api.model('Location Info Model', {
    'meta': fields.Nested(location_meta_fields, required=True),
    'data': fields.Nested(location_info_data_fields, required=True),
})

def location_info_to_csv(data):
    return meta_data_to_csv(data, location_meta_fields, location_info_data_fields)

# -------------------------------------------
# Location: children info
# -------------------------------------------
location_children_model = api.model('Location Children Info Model', {
    "results": fields.List(fields.Nested(location_info_model))
})

def location_children_to_csv(data):
    return meta_data_in_row_to_csv(data, location_meta_fields, location_info_data_fields)


# ------------------------------------------------------
# Location + Client: info
# ------------------------------------------------------
location_client_isp_info_model = api.model('Location Client ASN Model', {
    'meta': fields.Nested(location_client_meta_fields, required=True),
    'data': fields.Nested(location_info_data_fields, required=True)
})

def location_client_isp_info_to_csv(data):
    return meta_data_to_csv(data, location_client_meta_fields, location_info_data_fields)


# -------------------------------------------
# Locations: metrics
# -------------------------------------------
location_metric_model = api.model('Location Metric Model', {
    'meta': fields.Nested(location_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def location_metric_to_csv(data):
    return meta_results_to_csv(data, location_meta_fields, metric_data_fields)

# -------------------------------------------
# Location + Clients: metrics
# -------------------------------------------
location_client_metric_model = api.model('Location+Client Metric Model', {
    'meta': fields.Nested(location_client_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def location_client_metric_to_csv(data):
    return meta_results_to_csv(data, location_client_meta_fields, metric_data_fields)


# -------------------------------------------
# Location + Server: metrics
# -------------------------------------------
location_server_metric_model = api.model('Location+Server Metric Model', {
    'meta': fields.Nested(location_server_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def location_server_metric_to_csv(data):
    return meta_results_to_csv(data, location_server_meta_fields, metric_data_fields)


# -------------------------------------------
# Location + Client + Server: metrics
# -------------------------------------------
location_client_server_metric_model = api.model('Location+Client+Server Metric Model', {
    'meta': fields.Nested(location_client_server_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def location_client_server_metric_to_csv(data):
    return meta_results_to_csv(data, location_client_server_meta_fields, metric_data_fields)
