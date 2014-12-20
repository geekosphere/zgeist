# -*- coding: utf-8 -*-
# For a detailed description of every task:
#  https://github.com/geekosphere/zgeist/wiki/Tasks

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

    def delegate(item_id, url):
        return False

tasks = UrlTasks()

@celery.task
def discover(item_id, urls):
    '''Discover and delegate urls.'''
    logger.info('discover [item_id: {}, urls: {}]'.format(item_id, urls))

    for url in urls:
        task = tasks.get_task_for_url(url)
        task = task if task else generic

        generic.delay(item_id, url)
        #pika.emit('item.url_delegated', item_id=item_id, url=url, task=task.__name__)

@celery.task
def generic(item_id, url):
    '''Fetch magic numbers to determine the file type and proceed.'''
    logger.info('generic [item_id: {}, url: {}]'.format(item_id, url))

    content = crawl.get_first_bytes(url, image.tasks.max_siglength)

    task = image.tasks.get_task_for_content(content)

    if not task and util.valid_text(content):
        task = web.default

    if task: task.delay(item_id, url)

@celery.task
@tasks.by_domain(u'youtu.be')
@tasks.by_domain(u'youtube.com')
def youtube(item_id, url):
    logger.info('youtube: {}'.format(item))



