"""
Models used in deserialization of API.
"""

from flask_restplus import fields
from mlab_api.rest_api import api

# ---
# Base Models
# ---
base_meta_fields = api.model('Base Meta', {
    'client_continent': fields.String(description="Parent continent of Location."),
    'client_country': fields.String(description="Parent country of Location."),
    'client_region': fields.String(description="Parent region of Location."),
    'client_city': fields.String(description="Name of city, if location is a city."),
})

# ---
# Models for Location Search
# ---
search_meta_fields = base_meta_fields.extend('Search Meta', {
    'location': fields.String(description="Name of location."),
    'location_key': fields.String(description="Reverse Location name key."),
    'type': fields.String(description="Location type. city, region, country, or continent.")
})

# TODO: don't know why it won't register extended models
api.models[search_meta_fields.name] = search_meta_fields



search_data_fields = api.model('Search Data', {
    'last_three_month_test_count': fields.Integer(description="Test counts over last 3 months."),
    'test_count': fields.Integer(description="Test counts over entire MLab dataset")
})


search_result_fields = api.model('Search Result', {
    'meta': fields.Nested(search_meta_fields, required=True),
    'data': fields.Nested(search_data_fields, required=True)
})

location_search_model = api.model('Location Search Model', {
    'results': fields.List(fields.Nested(search_result_fields), required=True)
})

# ---
# Models for Location Metrics
# ---
metric_meta_fields = search_meta_fields.extend('Metric Meta', {
    'client_continent_code': fields.String(description="Internal continent code."),
    'client_country_code': fields.String(description="Internal country code."),
    'client_region_code': fields.String(description="Internal region code.")
})

api.models[metric_meta_fields.name] = metric_meta_fields


metric_data_fields = api.model('Metric Data', {
    'count': fields.Integer(description="Test counts for time period"),
    'date': fields.String(description="Date Aggregation.", required=True),
    'hour': fields.String(description="Hour Aggregation, if requested by hour."),
    'download_speed_mbps_median': fields.Float,
    'upload_speed_mbps_median': fields.Float
})

location_metric_model = api.model('DDD Location Metric Model', {
    'meta': fields.Nested(metric_meta_fields, required=True),
    'metrics': fields.List(fields.Nested(metric_data_fields), required=True)
})
