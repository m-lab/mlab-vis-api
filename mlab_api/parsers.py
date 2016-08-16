from flask_restplus import reqparse

date_arguments = reqparse.RequestParser()
date_arguments.add_argument('startdate', type=str, required=False, help='Start date of metrics')
date_arguments.add_argument('enddate', type=str, required=False, help='End date of metrics')
