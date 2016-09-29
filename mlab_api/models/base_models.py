# -*- coding: utf-8 -*-
'''
Base models to sub-class or clone
'''
from flask_restplus import fields
from mlab_api.rest_api import api

# ---
# Base Models
# ---
location_base_meta_fields = api.model('Base Meta', {
    'id': fields.Raw(description="Location id", attribute='client_location_key'),
    'type': fields.String(description="Location type. city, region, country, or continent."),
    'client_location_key': fields.String(description="Location ID."),
    'client_continent': fields.String(description="Continent of Location."),
    'client_continent_code': fields.String(description="Continent code of Location."),
    'client_country': fields.String(description="Country of Location."),
    'client_country_code': fields.String(description="Country code of Location."),
    'client_region': fields.String(description="Region of Location."),
    'client_region_code': fields.String(description="Region code of Location."),
    'client_city': fields.Raw(description="Name of city, if location is a city.")
})


search_data_fields = api.model('Search Data', {
    'last_three_month_test_count': fields.Integer(description="Test counts over last 3 months."),
    'test_count': fields.Integer(description="Test counts over entire MLab dataset"),
    'last_year_test_count': fields.Integer(description="Test counts over last year.")
})

metric_data_fields = api.model('Metric Data', {
    'count': fields.Integer(description="Test counts for time period."),
    'rtt_avg': fields.Float(description="Average round trip time"),
    'retransmit_avg': fields.Integer(description="Average retransmit rate."),
    'download_speed_mbps_median': fields.Integer(description="Median Download Speed."),
    'upload_speed_mbps_median': fields.Integer(description="Median Upload Speed."),
    'hour': fields.String(description="Hour Aggregation, if requested by hour."),
    'date': fields.String(description="Date for time period")
})
