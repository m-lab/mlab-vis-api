# -*- coding: utf-8 -*-
'''
Base models to sub-class or clone
'''
from flask_restplus import fields
from mlab_api.rest_api import api

# ---
# Base Models
# ---
base_meta_fields = api.model('Base Meta', {
    'client_continent': fields.String(description="Continent of Location."),
    'client_continent_code': fields.String(description="Continent code of Location."),
    'client_country': fields.String(description="Country of Location."),
    'client_country_code': fields.String(description="Country code of Location."),
    'client_region': fields.String(description="Region of Location."),
    'client_region_code': fields.String(description="Region code of Location."),
    'client_city': fields.String(description="Name of city, if location is a city.")
})


search_data_fields = api.model('Search Data', {
    'last_three_month_test_count': fields.Integer(description="Test counts over last 3 months."),
    'test_count': fields.Integer(description="Test counts over entire MLab dataset")
})
