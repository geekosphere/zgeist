# -*- coding: utf-8 -*-

import re
import os
import math
import urllib
import urlparse
import datetime
from copy import deepcopy
from os.path import join, dirname, abspath, realpath

import pytz
import yaml
from flask import request

def approot(*path):
    return realpath(join(dirname(abspath(__file__)), '..', *path))

def utcnow():
    """A timezone aware version of datetime.utcnow()"""
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

def dict_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def url_merge_param(url, params={}):
    """Returns a url with the specified params merged."""
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

valid_url_regexp = re.compile(
    r'^(?:http)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
def is_valid_url(url):
    return valid_url_regexp.match(url)

class Pagination(object):
    """Pagination for sqlalchemy queries."""
    def __init__(self, query, per_page=10):
        self._per_page = int(request.args.get('per_page', per_page))
        if self._per_page > 250: self._per_page = per_page

        # TODO: this is really slow compared to a func.count()!
        self._items = query.count()
        self._pages = int(math.ceil(self._items / self._per_page)) + 1

        # current page parameter (starts with 1)
        self._current = int(request.args.get('page', '1'))

        self._res = query.offset(self._current * self._per_page - self._per_page).limit(self._per_page).all()

    def __iter__(self):
        return self._res.__iter__()

    def __len__(self):
        return self._per_page

    def page_url(self, page):
        """Returns the current request url with page added as a parameter.""" 
        return url_merge_param(request.url, {'page': str(page)})

    def get_next(self):
        if self._current >= self._pages: return None
        return self.page_url(self._current+1)

    def get_prev(self):
        if self._current <= 1: return None
        return self.page_url(self._current-1)

    def get_links(self):
        if self._pages == 1: return
        def link_tuple(num=None):
            if not num:
                return (None, u'…')
            elif num == self._current:
                return (None, str(num))
            else:
                return (self.page_url(num), str(num))

        yield link_tuple(1)

        if self._current > 2:
            yield link_tuple() # ...
            if self._current == self._pages and self._pages > 3:
                yield link_tuple(self._current - 2)
            yield link_tuple(self._current - 1)

        if self._current != 1 and self._current != self._pages:
            yield link_tuple(self._current)

        if self._current < self._pages - 1:
            yield link_tuple(self._current + 1)
            if self._current == 1 and self._pages > 3:
                yield link_tuple(self._current + 2)
            yield link_tuple() # ...

        yield link_tuple(self._pages)

class ConfigAccessor(object):
    def __init__(self, local_file='local.yaml'):
        self._data = self._load('config.yaml')
        local = self._load(local_file)
        self._data = dict_merge(self._data, local)

    def _load(self, filename):
        filename = approot(filename)
        if not os.path.isfile(filename): return {}
        with open(filename, 'r') as f:
            contents = f.read().replace('%approot%', approot())
            return yaml.load(contents)

    def __getitem__(self, key):
        """Allows to use dot syntax in array accessor operator [] for read access.

        Like ``config['database.uri']`` to access ``self._data['database']['uri']``.
        """
        return reduce(lambda d, k: d[k], key.split('.'), self._data)

