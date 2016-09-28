# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function

from flask import Flask

app = Flask(__name__) #pylint: disable=C0103
app.config.from_object('config')
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config['RESTPLUS_VALIDATE'] = True
