# -*- coding: utf-8 -*-
'''
Models for location metrics
'''
from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.format_utils import convert_to_csv

from mlab_api.models.base_models import location_base_meta_fields, metric_data_fields

metric_meta_fields = location_base_meta_fields.extend('Location Metric Meta', {
})
api.models[metric_meta_fields.name] = metric_meta_fields

location_metric_model = api.model('Location Metric Model', {
    'meta': fields.Nested(metric_meta_fields, required=True),
    'results': fields.List(fields.Nested(metric_data_fields), required=True)
})

def location_metric_to_csv(data):
    rows = [{
                'count': row['count']
            } for row in data['results']]
    fieldnames = ['count']
    csv = convert_to_csv(rows, fieldnames)
    print('got csv', csv)
    return csv
