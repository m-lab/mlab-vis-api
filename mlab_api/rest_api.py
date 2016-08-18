# -*- coding: utf-8 -*-
'''
Setup API instance.
'''
import logging
from flask_restplus import Api

# This is connected to the app in
# main.py
api = Api(version='0.1.0', doc='/', title='MLab API')

@api.errorhandler
def server_error(err):
    """
    Handle error during request.
    """
    logging.exception('An error occurred during a request.')
    logging.exception(err)
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500
