# -*- coding: utf-8 -*-
'''
Models for definging return value of Server specific calls
'''

from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.format_utils import meta_results_to_csv, meta_data_in_row_to_csv, \
    meta_data_to_csv

from mlab_api.models.base_models import search_data_fields, metric_data_fields, \
    server_search_meta_fields, server_meta_fields

# -------------------------------------------
# Servers: search
# -------------------------------------------
server_search_result_fields = api.model('Server ASN Search Result', {
    'meta': fields.Nested(server_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

server_search_model = api.model('Server ASN Search Results', {
    'results': fields.List(fields.Nested(server_search_result_fields), required=True)
})


def server_search_to_csv(data):
    return meta_data_in_row_to_csv(data, server_search_meta_fields, search_data_fields)


# -------------------------------------------
# Servers: info
# -------------------------------------------
server_info_model = api.model('Server Info Model', {
    'meta': fields.Nested(server_search_meta_fields, required=True),
})

def server_info_to_csv(data):
    return meta_data_to_csv(data, server_meta_fields, server_info_data_fields)


# -------------------------------------------
# Servers: metrics
# -------------------------------------------
server_metric_model = api.model('Server Metric Model', {
    'meta': fields.Nested(server_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def server_metric_to_csv(data):
    return meta_results_to_csv(data, server_meta_fields, metric_data_fields)
