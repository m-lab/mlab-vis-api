from flask_restplus import fields
from mlab_api.rest_api import api

from mlab_api.models.base_models import base_meta_fields



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
