# -*- coding: utf-8 -*-

import logging
import time

from zgeist import celery

logger = logging.getLogger('zgeist.task.url')

class UrlTasks(object):
    def __init__(self):
        self.patterns = []
        self.domains = []

    def by_pattern(self, pattern):
        def decorator(function):
            self.patterns.append((pattern, function))
            return function
        return decorator

    def by_domain(self, domain):
        def decorator(function):
            self.domains.append((domain, function))
            return function
        return decorator

tasks = UrlTasks()

@celery.task
def discover(item):
    logger.info('discover: {}'.format(item))
    logger.info('discover executed')
    youtube.delay(item)

@celery.task
@tasks.by_pattern(r'youtu\.be')
def youtube(item):
    logger.info('youtube: {}'.format(item))



