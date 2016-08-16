from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.models.base_models import base_meta_fields

# ---
# Models for Location Metrics
# ---
metric_meta_fields = base_meta_fields.extend('Metric Meta', {
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

location_metric_model = api.model('Location Metric Model', {
    'meta': fields.Nested(metric_meta_fields, required=True),
    'metrics': fields.List(fields.Nested(metric_data_fields), required=True)
})
