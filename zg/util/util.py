"""
Utility Functions
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import os
import re
import sys
import urllib
import urlparse
import hashlib
import datetime
from copy import deepcopy
from os.path import join, dirname, abspath, realpath
from collections import OrderedDict
from webassets.loaders import YAMLLoader
import pytz
import yaml

default_env = 'test' if sys.argv[0].endswith('nosetests') else 'development'

#: environment set using ENV, ``production``, ``development`` or ``test``.
environment = os.environ.get('ENV', default_env)

def root(*path):
    """Returns the application root with optional postfix paths."""
    return realpath(join(dirname(abspath(__file__)), '../..', *path))

def utcnow():
    """Returns a timezone aware version of datetime.utcnow()"""
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

def dict_merge(a, b):
    """
    Recursively merge two dictionaries.

    Not just a simple ``a['key'] = b['key']``, if both a and b
    have a key whos value is a dict then dict_merge is called
    on both values and the result stored in the returned
    dictionary.
    """
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def unique(things):
    """Returns a unique version of things."""
    return list(OrderedDict.fromkeys(things))

def uri_param_merge(uri, params={}):
    """Returns the uri with the specified parameters merged."""
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)

url_regexp = re.compile(
    r'^(?:http)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def url_valid(url):
    """Check if the specified url is valid."""
    return url_regexp.match(url)

class DictAssetLoader(YAMLLoader):
    def __init__(self, obj):
        self._obj = obj

    def load_bundles(self, environment=None):
        return self._get_bundles(self._obj, environment)

#: IEC binary prefixes
IEC_PREFIX=['B']+[u + 'iB' for u in list('KMGTPEZY')]

def to_bytes(s):
    """Parses s to a int of bytes."""
    (value, label) = re.match(r'^([\d.]+) ?((?:[KMGTPEZY]i)?B)$', s).groups()
    return int(float(value) * 1024**IEC_PREFIX.index(label))

def format_bytes(size, labels=IEC_PREFIX):
    """Returns a human readable version of a size in bytes."""
    if size > 1024 and len(labels) > 0:
        return format_bytes(size / 1024.0, labels[1:])
    else:
        return '{:.2f}{}'.format(size, labels[0])

def md5file(filename, blocksize=2**20):
    """Returns the md5sum of a local file (cryptographically insecure)."""
    m = hashlib.md5()
    with open(filename, 'r') as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()

def sha512file(filename, blocksize=2**20):
    """Returns the sha512sum of a local file (cryptographically secure)."""
    m = hashlib.sha512()
    with open(filename, 'r') as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()

