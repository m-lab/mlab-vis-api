# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function
import os
import logging

from flask_restplus import cors

# Import Configured Flask App
from mlab_api.app import app

# Import namespaces
from mlab_api.endpoints.locations import LOCATIONS_NS
from mlab_api.endpoints.debug import DEBUG_NS
from mlab_api.endpoints.clients import CLIENT_ASN_NS
from mlab_api.endpoints.servers import SERVER_ASN_NS
from mlab_api.endpoints.raw import RAW_NS
from mlab_api.decorators import format_from_url_decorator, download_decorator

# API is defined here
from mlab_api.rest_api import API

ROOT = logging.getLogger()
ROOT.setLevel(logging.DEBUG)

# This provides CORS for all API Requests and adds in our media type coercing
# based on `format`
API.decorators = [cors.crossdomain(origin='*'), format_from_url_decorator,
                  download_decorator]

# Add namespaces defined in endpoints module
API.add_namespace(LOCATIONS_NS)
API.add_namespace(CLIENT_ASN_NS)
API.add_namespace(SERVER_ASN_NS)
API.add_namespace(RAW_NS)

# init API with Flask App
API.init_app(app)

DEBUG_FLAG = False
API_MODE = os.environ.get("API_MODE")
print(API_MODE)

if API_MODE == 'staging' or API_MODE == 'sandbox':
    DEBUG_FLAG = True
    API.add_namespace(DEBUG_NS)
else:
    DEBUG_FLAG = False

if __name__ == '__main__':
    app.run(port=8080, debug=DEBUG_FLAG)
