"""
Configuration Accessor
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import os
import yaml
from .util import root, dict_merge, environment

class ConfigAccessor(object):
    _instance = None

    def __init__(self):
        self._data = {}

    def load(self, filename):
        path = root('conf', filename)

        if not os.path.isfile(path):
            return

        with open(path) as file:
            content = file.read().replace('%root%', root())
            self.merge(yaml.load(content))

    def merge(self, other):
        self._data = dict_merge(self._data, other)

    def __getitem__(self, key):
        """
        Retrieve a deeply nested value from the configuration.
        
        Like ``accessor['database.uri']`` to access
        ``accessor._data['database']['uri']``.
        """
        try:
            return reduce(lambda d, k: d[k], key.split('.'), self._data)
        except:
            return None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ConfigAccessor()
            cls._instance.load('main.yml')
            cls._instance.load('{}.yml'.format(environment))
        return cls._instance

def config(key, default=None):
    accessor = ConfigAccessor.instance()
    value = accessor[key]
    if value != None:
        return value
    else:
        return default

import logging.config
logging.config.dictConfig(config('logger'))

