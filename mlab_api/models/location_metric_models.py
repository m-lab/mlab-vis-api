# -*- coding: utf-8 -*-
'''
Models for location metrics
'''
from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.format_utils import meta_results_to_csv

from mlab_api.models.base_models import location_meta_fields, metric_data_fields, \
    location_client_meta_fields, location_server_meta_fields, location_client_server_meta_fields

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
