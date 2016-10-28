# -*- coding: utf-8 -*-
'''
Provide instance of analytics to track events and timings.
'''
from mlab_api.analytics.google_analytics import GoogleAnalyticsClient
from mlab_api.app import app

tracking_id = app.config['GA_TRACKING_ID']

analytics = GoogleAnalyticsClient(tracking_id)
