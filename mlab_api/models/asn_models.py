# -*- coding: utf-8 -*-

from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.models.base_models import search_data_fields

# ---
# Models for Client ASN
# ---
client_asn_search_meta_fields = api.model('Client ASN Search Meta', {
    'client_asn_name': fields.String(description="Name of ASN."),
    'client_asn_name_lookup': fields.String(description="Key used to look up ASN."),
    'client_asn_number': fields.String(description="ASN number.")
})

client_asn_search_result_fields = api.model('Client ASN Search Result', {
    'meta': fields.Nested(client_asn_search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

client_asn_search_model = api.model('Client ASN Search Results', {
    'results': fields.List(fields.Nested(client_asn_search_result_fields), required=True)
})
