# -*- coding: utf-8 -*-
'''
Models for definging return value of Client / Server specific calls
'''

from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.models.base_models import search_data_fields, metric_data_fields, \
    client_search_meta_fields, server_search_meta_fields, client_meta_fields, \
    server_meta_fields


# ---
# Models for Client ASN
# ---
client_search_result_fields = api.model('Client ASN Search Result', {
    'meta': fields.Nested(client_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

client_search_model = api.model('Client ASN Search Results', {
    'results': fields.List(fields.Nested(client_search_result_fields), required=True)
})

client_info_model = api.model('Client Info Model', {
    'meta': fields.Nested(client_search_meta_fields, required=True),
})

# --
# Client Metrics
# --
client_metric_model = api.model('Client Metric Model', {
    'meta': fields.Nested(client_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

# -----------------------------------

# ---
# Models for Server ASN
# ---

server_search_result_fields = api.model('Server ASN Search Result', {
    'meta': fields.Nested(server_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

server_search_model = api.model('Server ASN Search Results', {
    'results': fields.List(fields.Nested(server_search_result_fields), required=True)
})

server_info_model = api.model('Server Info Model', {
    'meta': fields.Nested(server_search_meta_fields, required=True),
})

# --
# Server Metrics
# --

server_metric_model = api.model('Server Metric Model', {
    'meta': fields.Nested(server_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})
