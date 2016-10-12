# -*- coding: utf-8 -*-
'''
Models for definging return value of location info api call
'''
from flask_restplus import fields
from mlab_api.rest_api import api


from mlab_api.models.base_models import location_meta_fields, location_client_meta_fields

from mlab_api.format_utils import meta_data_to_csv, meta_data_in_row_to_csv, meta_in_row_to_csv

# -------------------------------------------
# Location Info
# -------------------------------------------
location_info_model = api.model('Location Info Model', {
    'meta': fields.Nested(location_meta_fields, required=True),
    'data': fields.Nested(location_info_data_fields, required=True),
})

def location_info_to_csv(data):
    return meta_data_to_csv(data, location_meta_fields, location_info_data_fields)

# -------------------------------------------
# Location Children Info
# -------------------------------------------
location_children_model = api.model('Location Children Info Model', {
    "results": fields.List(fields.Nested(location_info_model))
})

def location_children_to_csv(data):
    return meta_data_in_row_to_csv(data, location_meta_fields, location_info_data_fields)


# ------------------------------------------------------
# Location + Client Info
# ------------------------------------------------------
location_client_isp_info_model = api.model('Location Client ASN Model', {
    'meta': fields.Nested(location_client_meta_fields, required=True),
    'data': fields.Nested(location_info_data_fields, required=True)
})

def location_client_isp_info_to_csv(data):
    return meta_data_to_csv(data, location_client_meta_fields, location_info_data_fields)
