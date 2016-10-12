# -*- coding: utf-8 -*-
'''
Models for Location Search
'''
from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.format_utils import meta_data_in_row_to_csv, meta_in_row_to_csv

from mlab_api.models.base_models import location_search_meta_fields, search_data_fields, \
                                        location_client_meta_fields, location_server_meta_fields

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
# Location + Client List
# ------------------------------------------------------
location_client_list_model = api.model('Location Client List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(location_client_meta_fields, required=True)
    }))
})

def location_client_list_to_csv(data):
    return meta_in_row_to_csv(data, location_client_meta_fields)


# ------------------------------------------------------
# Location + Server List
# ------------------------------------------------------
location_server_list_model = api.model('Location Server List Model', {
    "results": fields.List(fields.Nested({
        'meta': fields.Nested(location_server_meta_fields, required=True)
    }))
})

def location_server_list_to_csv(data):
    return meta_in_row_to_csv(data, location_server_meta_fields)
