# -*- coding: utf-8 -*-
'''
Google analytics timer + tracking
'''

from __future__ import with_statement
from functools import wraps
import time

from UniversalAnalytics import Tracker

class Timer(object):
    '''
    A context manager/decorator for analytics.timing().
    '''

    def __init__(self, client, category, variable, label=None):
        self.client = client
        self.category = category
        self.variable = variable
        self.label = label
        self.milliseconds = None
        self._sent = False
        self._start_time = None

    def __call__(self, func):
        '''
        Thread-safe timing function decorator.
        '''
        @wraps(func)
        def _wrapped(*args, **kwargs):
            '''
            Wrapped call function
            '''
            start_time = time.time()
            try:
                return_value = func(*args, **kwargs)
            finally:
                elapsed_time_milliseconds = 1000.0 * (time.time() - start_time)
                self.client.timing(self.category, self.variable,
                                   self.label, elapsed_time_milliseconds)
            return return_value
        return _wrapped

    def __enter__(self):
        return self.start()

    def __exit__(self, typ, value, table):
        self.stop()

    def start(self):
        '''
        Start timer
        '''
        self.milliseconds = None
        self._sent = False
        self._start_time = time.time()
        return self

    def stop(self, send=True):
        '''
        Stop timer
        '''
        if self._start_time is None:
            raise RuntimeError('Timer has not started.')
        delta = time.time() - self._start_time
        self.milliseconds = 1000.0 * delta  # Convert to milliseconds.
        if send:
            self.send()
        return self

    def send(self):
        '''
        Send collected timing data
        '''
        if self.milliseconds is None:
            raise RuntimeError('No data recorded.')
        if self._sent:
            raise RuntimeError('Already sent data.')
        self._sent = True
        self.client.timing(self.category, self.variable, self.label,
                           self.milliseconds)

class GoogleAnalyticsClient(object):
    '''
    Analytics timing / event client
    '''

    def __init__(self, ua_id):
        self.tracker = Tracker.create(ua_id, client_id='zzz')

    def timer(self, category, variable, label=None):
        '''
        Initializes a timer class
        '''
        return Timer(self, category, variable, label)

    def timing(self, category, variable, label, timed_amount):
        '''
        Send new timing information. `timed_amount` is in milliseconds.
        '''

        # google analytics requires integers for timing?
        timed_amount = int(round(timed_amount))

        self.tracker.send('timing', category, variable, timed_amount, label)


    def event(self, category, action, label=None, value=None):
        '''
        Set a set value.
        '''
        self.tracker.send('event', category, action, label, value)
