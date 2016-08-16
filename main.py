# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function
from flask_restplus import cors

# Import Configured Flask App
from mlab_api.app import app

# Import namespaces
from mlab_api.endpoints.locations import locations_ns
from mlab_api.endpoints.debug import debug_ns

# API is defined here
from mlab_api.rest_api import api

# This appears to provide CORS for all API Requests
api.decorators = [cors.crossdomain(origin='*')]

# Add namespaces defined in endpoints module
api.add_namespace(locations_ns)
api.add_namespace(debug_ns)

# init api with Flask App
api.init_app(app)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
