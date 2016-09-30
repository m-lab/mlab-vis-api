# -*- coding: utf-8 -*-
'''
Models for definging return value of Client / Server specific calls
'''

from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.models.base_models import search_data_fields, metric_data_fields

# ---
# Models for Client ASN
# ---
client_asn_search_meta_fields = api.model('Client ASN Search Meta', {
    'client_asn_name': fields.Raw(description="Name of ASN."),
    'client_asn_number': fields.String(description="ASN number."),
    'id': fields.String(description="ID for ASN", attribute='client_asn_number'),
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'test_count': fields.Integer(description="All Test counts")
})

client_asn_search_result_fields = api.model('Client ASN Search Result', {
    'meta': fields.Nested(client_asn_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

client_asn_search_model = api.model('Client ASN Search Results', {
    'results': fields.List(fields.Nested(client_asn_search_result_fields), required=True)
})

client_asn_info_model = api.model('Client Info Model', {
    'meta': fields.Nested(client_asn_search_meta_fields, required=True),
})

# --
# Client Metrics
# --

client_metric_meta_fields = api.model('Client ASN Metric Meta', {
    'client_asn_number': fields.String(description="Client ASN Number"),
    'client_asn_name': fields.Raw(description="Client ASN Name"),
    'id': fields.String(description="Client ID")
})

client_metric_model = api.model('Client Metric Model', {
    'meta': fields.Nested(client_metric_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

# -----------------------------------

# ---
# Models for Server ASN
# ---
server_asn_search_meta_fields = api.model('Server ASN Search Meta', {
    'server_asn_name': fields.Raw(description="Name of ASN."),
    'server_asn_number': fields.Raw(description="ASN for server"),
    'id': fields.Raw(description="Key used to look up ASN.", attribute='server_asn_number'),
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'test_count': fields.Integer(description="All Test counts")
})

server_asn_search_result_fields = api.model('Server ASN Search Result', {
    'meta': fields.Nested(server_asn_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

server_asn_search_model = api.model('Server ASN Search Results', {
    'results': fields.List(fields.Nested(server_asn_search_result_fields), required=True)
})

server_asn_info_model = api.model('Server Info Model', {
    'meta': fields.Nested(server_asn_search_meta_fields, required=True),
})

# --
# Server Metrics
# --
server_metric_meta_fields = api.model('Server ASN Metric Meta', {
    'server_asn_number': fields.String(description="Server ASN Number"),
    'server_asn_name': fields.Raw(description="Server ASN Name"),
    'id': fields.String(description="Server ID")
})

server_metric_model = api.model('Server Metric Model', {
    'meta': fields.Nested(server_metric_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})
