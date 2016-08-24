# -*- coding: utf-8 -*-
'''
Models for definging return value of location info api call
'''
from flask_restplus import fields
from mlab_api.rest_api import api


from mlab_api.models.base_models import base_meta_fields

location_info_meta_fields = base_meta_fields.extend('Location Info Meta', {
    'client_continent_code': fields.String(description="Internal continent code.", required=False),
    'client_country_code': fields.String(description="Internal country code.", required=False),
    'client_region_code': fields.String(description="Internal region code.", required=False)
})

api.models[location_info_meta_fields.name] = location_info_meta_fields

location_info_data_fields = api.model('Location Info Data', {
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'last_year_download_speed_mbps_median': fields.Float,
    'last_year_download_speed_mbps_avg': fields.Float,
    'last_year_download_speed_mbps_min': fields.Float,
    'last_year_download_speed_mbps_max': fields.Float,
    'last_year_download_speed_mbps_stddev': fields.Float,
    'last_year_upload_speed_mbps_median': fields.Float,
    'last_year_upload_speed_mbps_avg': fields.Float,
    'last_year_upload_speed_mbps_min': fields.Float,
    'last_year_upload_speed_mbps_max': fields.Float,
    'last_year_upload_speed_mbps_stddev': fields.Float,
    'rtt_avg': fields.Float,
    'retransmit_avg': fields.Float
})

location_info_model = api.model('Location Info Model', {
    'meta': fields.Nested(location_info_meta_fields, required=True),
    'data': fields.Nested(location_info_data_fields, required=True)
})

location_children_model = api.model('Location Children Info Model', {
    "results": fields.List(fields.Nested(location_info_model))
})
