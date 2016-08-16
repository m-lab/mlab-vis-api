from flask_restplus import fields
from mlab_api.rest_api import api

# ---
# Base Models
# ---
base_meta_fields = api.model('BASE Meta', {
    'client_continent': fields.String,
    'client_country': fields.String,
    'client_region': fields.String,
})

# ---
# Models for Location Search
# ---
search_meta_fields = base_meta_fields.extend('Search Meta', {
    'location': fields.String,
    'location_key': fields.String,
    'type': fields.String
})


search_data_fields = api.model('Search Data', {
    'last_three_month_test_count': fields.Integer,
    'test_count': fields.Integer
})


search_result_fields = api.model('Search Result', {
    'meta': fields.Nested(search_meta_fields),
    'data': fields.Nested(search_data_fields)
})

location_search_model = api.model('Location Search Model', {
    'results': fields.List(fields.Nested(search_result_fields))
})

# ---
# Models for Location Metrics
# ---
metric_meta_fields = api.model('DDDDD Metric Meta', {
    'client_city': fields.String,
    'client_continent_code': fields.String,
    'client_country_code': fields.String,
    'client_region_code': fields.String
})

metric_data_fields = api.model('DDD Metric Data', {
    'count': fields.Integer,
    'date': fields.String,
    'hour': fields.String,
    'download_speed_mbps_median': fields.Float,
    'upload_speed_mbps_median': fields.Float
})

location_metric_model = api.model('DDD Location Metric Model', {
    'meta': fields.Nested(metric_meta_fields),
    'metrics': fields.List(fields.Nested(metric_data_fields))
})
