# -*- coding: utf-8 -*-
#pylint: disable=no-name-in-module, relative-import
'''
App engine configuration
'''
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
