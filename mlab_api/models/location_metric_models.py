# -*- coding: utf-8 -*-
'''
Models for location metrics
'''
from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.models.base_models import base_meta_fields, metric_data_fields

metric_meta_fields = base_meta_fields.extend('Metric Meta', {
    'client_continent_code': fields.String(description="Internal continent code."),
    'client_country_code': fields.String(description="Internal country code."),
    'client_region_code': fields.String(description="Internal region code.")
})
api.models[metric_meta_fields.name] = metric_meta_fields

location_metric_model = api.model('Location Metric Model', {
    'meta': fields.Nested(metric_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})
