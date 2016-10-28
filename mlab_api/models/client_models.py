# -*- coding: utf-8 -*-
'''
Models for definging return value of Client specific calls
'''

from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.format_utils import meta_results_to_csv, meta_data_to_csv, \
    meta_data_in_row_to_csv, meta_in_row_to_csv

from mlab_api.models.base_models import search_data_fields, metric_data_fields, \
    client_search_meta_fields, client_meta_fields, client_server_meta_fields


# -------------------------------------------
# Clients: search
# -------------------------------------------
client_search_result_fields = api.model('Client ASN Search Result', {
    'meta': fields.Nested(client_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

client_search_model = api.model('Client ASN Search Results', {
    'results': fields.List(fields.Nested(client_search_result_fields), required=True)
})

def client_search_to_csv(data):
    return meta_data_in_row_to_csv(data, client_search_meta_fields, search_data_fields)


# ------------------------------------------------------
# Client + Server List
# ------------------------------------------------------
client_server_list_model = api.model('Client Server List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(client_server_meta_fields, required=True)
    }))
})

def client_server_list_to_csv(data):
    return meta_in_row_to_csv(data, client_server_meta_fields)


# -------------------------------------------
# Clients: info
# -------------------------------------------
client_info_model = api.model('Client Info Model', {
    'meta': fields.Nested(client_search_meta_fields, required=True),
})

def client_info_to_csv(data):
    return meta_data_to_csv(data, client_meta_fields, None)

# -------------------------------------------
# Clients: metrics
# -------------------------------------------
client_metric_model = api.model('Client Metric Model', {
    'meta': fields.Nested(client_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def client_metric_to_csv(data):
    return meta_results_to_csv(data, client_meta_fields, metric_data_fields)

# -------------------------------------------
# Clients + Servers: metrics
# -------------------------------------------
client_server_metric_model = api.model('Client+Server Metric Model', {
    'meta': fields.Nested(client_server_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def client_server_metric_to_csv(data):
    return meta_results_to_csv(data, client_server_meta_fields, metric_data_fields)
