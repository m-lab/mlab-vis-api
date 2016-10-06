# -*- coding: utf-8 -*-
'''
Setup API instance.
'''
import logging

from flask_restplus import Api
from flask import make_response

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



@api.representation('text/csv')
def csv_mediatype_representation(data, code, headers):
    """
    Assume the data is already marshalled to CSV and just write it
    to the response
    """
    print("handling CSV")
    print(data)
    resp = make_response(data, code)
    resp.headers.extend(headers)
    return resp

@api.representation('application/json')
def json_mediatype_representation(data, code, headers):
    """
    Assume the data is already marshalled to JSON and just write it
    to the response
    """
    print("handling JSON")
    print(data)
    if not isinstance(data, basestring):
        print("shit this isnt a string")
        data = "fake it homie."
    resp = make_response(data, code)
    resp.headers.extend(headers)
    print(resp.headers, headers)

    return resp
