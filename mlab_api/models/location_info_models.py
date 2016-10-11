# -*- coding: utf-8 -*-
'''
Models for definging return value of location info api call
'''
from flask_restplus import fields
from mlab_api.rest_api import api


from mlab_api.models.base_models import location_base_meta_fields
from mlab_api.format_utils import meta_data_to_csv, meta_data_in_row_to_csv

location_info_meta_fields = location_base_meta_fields.extend('Location Info Meta', {
    'id': fields.String(description="Location Id"),
    'client_location_key': fields.String(description="Location Id", attribute='id'),
    'location_key': fields.String(description="Location Id", attribute='id')
})
api.models[location_info_meta_fields.name] = location_info_meta_fields

location_info_data_base_fields = api.model('Base Location Info Data', {
    'last_year_download_speed_mbps_median': fields.Float,
    'last_year_download_speed_mbps_avg': fields.Float,
    'last_year_download_speed_mbps_min': fields.Float,
    'last_year_download_speed_mbps_max': fields.Float,
    'last_year_download_speed_mbps_stddev': fields.Float,
    'last_year_download_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of download speeds"),
    'last_year_upload_speed_mbps_median': fields.Float,
    'last_year_upload_speed_mbps_avg': fields.Float,
    'last_year_upload_speed_mbps_min': fields.Float,
    'last_year_upload_speed_mbps_max': fields.Float,
    'last_year_upload_speed_mbps_stddev': fields.Float,
    'last_year_upload_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of upload speeds"),
    'last_year_test_count': fields.Integer,
    'last_year_rtt_avg': fields.Float,
    'last_year_retransmit_avg': fields.Float,
})

location_info_data_fields = location_info_data_base_fields.extend('Location Info Data', {
    'last_year_test_count': fields.Integer(description="Test counts in last year")

})
api.models[location_info_data_fields.name] = location_info_data_fields


location_client_isp_data_fields = location_info_data_base_fields.extend('Location Info Meta', {
})
api.models[location_client_isp_data_fields.name] = location_client_isp_data_fields

location_info_model = api.model('Location Info Model', {
    'meta': fields.Nested(location_info_meta_fields, required=True),
    'data': fields.Nested(location_info_data_fields, required=True),
})


def location_info_to_csv(data):
    return meta_data_to_csv(data, location_info_meta_fields, location_info_data_fields)


location_children_model = api.model('Location Children Info Model', {
    "results": fields.List(fields.Nested(location_info_model))
})

def location_children_to_csv(data):
    return meta_data_in_row_to_csv(data, location_info_meta_fields, location_info_data_fields)


location_client_asn_meta_fields = location_info_meta_fields.extend('Location Client ASN Meta', {
    'client_asn_name': fields.String(description="Name of ASN."),
    'client_asn_number': fields.String(description="ASN number."),
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'location_key': fields.String(description="Location Id"),
    'id': fields.String(description="Location Id", attribute='location_key'),
    'client_location_key': fields.String(description="Location Id", attribute='location_key')
})

api.models[location_client_asn_meta_fields.name] = location_client_asn_meta_fields

location_client_isp_info_model = api.model('Location Client ASN Model', {
    'meta': fields.Nested(location_client_asn_meta_fields, required=True),
    'data': fields.Nested(location_client_isp_data_fields, required=True)
})

def location_client_isp_info_to_csv(data):
    return meta_data_to_csv(data, location_client_asn_meta_fields, location_client_isp_data_fields)
