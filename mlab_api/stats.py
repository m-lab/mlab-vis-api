# -*- coding: utf-8 -*-
import requests
from statsd import StatsClient

from mlab_api.app import app

host = app.config['STATSD_SERVER']
if not host:
    host = 'localhost'


#Instance of statsd client to import
statsd = StatsClient(host=host, prefix="mlab")

tracking_id = app.config['GA_TRACKING_ID']


def track_event(category, action, label=None, value=0):
    data = {
        'v': '1',  # API Version.
        'tid': tracking_id,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': '555',
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
    }

    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)

    # If the request fails, this will raise a RequestException. Depending
    # on your application's needs, this may be a non-error and can be caught
    # by the caller.
    response.raise_for_status()
