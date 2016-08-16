# -*- coding: utf-8 -*-
'''
API input parameter parsers.
'''
from flask_restplus import reqparse

# date arguments allow for start and end dates
# defaults are provided in config
date_arguments = reqparse.RequestParser()
date_arguments.add_argument('startdate', type=str, required=False, help='Start date of metrics')
date_arguments.add_argument('enddate', type=str, required=False, help='End date of metrics')
