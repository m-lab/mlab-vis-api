# -*- coding: utf-8 -*-
'''
Models for Location Search
'''
from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.models.base_models import base_meta_fields, search_data_fields

search_meta_fields = base_meta_fields.extend('Search Meta', {
    'location': fields.Raw(description="Name of location."),
    'location_key': fields.Raw(description="Location name key."),
    'id': fields.Raw(description="Location id", attribute='location_key'),
    'type': fields.String(description="Location type. city, region, country, or continent.")
})

# HACK: don't know why it won't register extended models
# so we need to do it manually here.
api.models[search_meta_fields.name] = search_meta_fields

search_result_fields = api.model('Search Result', {
    'meta': fields.Nested(search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

location_search_model = api.model('Location Search Model', {
    'results': fields.List(fields.Nested(search_result_fields), required=True)
})
