# -*- coding: utf-8 -*-
from statsd import StatsClient

from mlab_api.analytics.google_analytics import GoogleAnalyticsClient
from mlab_api.app import app

host = app.config['STATSD_SERVER']
if not host:
    host = 'localhost'


#Instance of statsd client to import
statsd = StatsClient(host=host, prefix="mlab")

tracking_id = app.config['GA_TRACKING_ID']

analytics = GoogleAnalyticsClient(tracking_id)
