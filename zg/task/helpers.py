"""
Helpers used for celery tasks.
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from zg.util import config, to_bytes, format_bytes, mktemp
from urlparse import urlparse
from zg.app import celery
from mock import Mock
import re
import os
import os.path
import logging

logger = logging.getLogger('zg.task.helpers')

class TaskMapper(object):
    def __init__(self):
        self.patterns = []
        self.domains = []
        self.mimetypes = []

    def by_pattern(self, pattern):
        def decorator(func):
            self.patterns.append((pattern, func))
            return func
        return decorator

    def by_domain(self, domain):
        def decorator(func):
            self.domains.append((domain, func))
            return func
        return decorator

    def by_mimetype(self, mimetype):
        def decorator(func):
            pattern = '^{}$'.format(mimetype.replace('*', '[^/]+'))
            self.mimetypes.append((pattern, func))
            return func
        return decorator

    def get_task_by_pattern(self, url):
        return next((f for (p, f) in self.patterns if re.findall(p, url)), None)

    def get_task_by_domain(self, url):
        url_domain = urlparse(url).hostname
        return next((f for (d, f) in self.domains if d == url_domain), None)

    def get_task_by_mimetype(self, mimetype):
        return next((f for (m, f) in self.mimetypes if re.findall(m, mimetype)), None)

    def get_task_for_url(self, url):
        return self.get_task_by_pattern(url) or self.get_task_by_domain(url)

    def get_task_for_mimetype(self, mimetype):
        return self.get_task_by_mimetype(mimetype)

class MockTask(object):
    def __init__(self, name):
        self.name = name
        self.mock = Mock()

    def __enter__(self):
        self.old = celery.tasks[self.name]
        celery.tasks[self.name] = self.mock
        return self.mock

    def __exit__(self, type, value, traceback):
        celery.tasks[self.name] = self.old

