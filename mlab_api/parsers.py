# -*- coding: utf-8 -*-
'''
API input parameter parsers.
'''
from flask_restplus import reqparse
from mlab_api.constants import FILTER_TYPES, TIME_BINS

# date arguments allow for start and end dates
# defaults are provided in config
date_arguments = reqparse.RequestParser()
date_arguments.add_argument('startdate', type=str, required=False, help='Start date of metrics')
date_arguments.add_argument('enddate', type=str, required=False, help='End date of metrics')
date_arguments.add_argument('timebin', type=str, required=True,
                            choices=TIME_BINS.keys(),
                            help='Time binning to use for time metrics')


type_arguments = reqparse.RequestParser()
type_arguments.add_argument('type', type=str, required=False,
                            choices=['country', 'region', 'city'],
                            help='Limit results to a specific type')


include_data_arguments = reqparse.RequestParser()
include_data_arguments.add_argument('data', type=bool, required=False, default=False, help='Include data attributes in results')


search_arguments = reqparse.RequestParser()
search_arguments.add_argument('q', type=str, required=True,
                              help='Query String')
search_arguments.add_argument('filtertype', type=str, required=False,
                              choices=FILTER_TYPES,
                              help='Filter type works in conjunction with filtervalue to specify search filter')

search_arguments.add_argument('filtervalue', type=str, required=False,
                              help='Limit search to only results with associations with ids in filtervalue. Id type is specified in filtertype.')


top_arguments = reqparse.RequestParser()
top_arguments.add_argument('limit', type=int, required=False,
                            help='Limits results count to top number' )

top_arguments.add_argument('filtertype', type=str, required=True,
                              choices=FILTER_TYPES,
                              help='Filter type works in conjunction with filtervalue to specify search filter')

top_arguments.add_argument('filtervalue', type=str, required=True,
                              help='Limit search to only results with associations with ids in filtervalue. Id type is specified in filtertype.')
