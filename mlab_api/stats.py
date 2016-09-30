# -*- coding: utf-8 -*-
from statsd import StatsClient

from mlab_api.app import app

host = app.config['STATSD_SERVER']
if not host:
    host = 'localhost'


#Instance of statsd client to import
statsd = StatsClient(host=host, prefix="mlab")
