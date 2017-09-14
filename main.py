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
from mlab_api.endpoints.locations import locations_ns
from mlab_api.endpoints.debug import debug_ns
from mlab_api.endpoints.clients import client_asn_ns
from mlab_api.endpoints.servers import server_asn_ns
from mlab_api.endpoints.raw import raw_ns

from mlab_api.decorators import format_from_url_decorator, download_decorator

# API is defined here
from mlab_api.rest_api import api

root = logging.getLogger()
root.setLevel(logging.DEBUG)

# This provides CORS for all API Requests and adds in our media type coercing based on `format`
api.decorators = [cors.crossdomain(origin='*'), format_from_url_decorator, download_decorator]

# Add namespaces defined in endpoints module
api.add_namespace(locations_ns)
api.add_namespace(client_asn_ns)
api.add_namespace(server_asn_ns)
api.add_namespace(raw_ns)

# init api with Flask App
api.init_app(app)

debug_flag = False
api_mode = os.environ.get("API_MODE")

if api_mode == 'DEV':
    print('DEV MODE')
    debug_flag = True
    api.add_namespace(debug_ns)
else:
    print('PRODUCTION MODE')
    debug_flag = False

if __name__ == '__main__':
    app.run(port=8080, debug=debug_flag)
