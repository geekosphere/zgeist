from __future__ import division, print_function, absolute_import, unicode_literals
import os
import re
import logging
import requests
from .config import config
from . import mktemp, to_bytes, format_bytes, md5file

# disables SSL verification failure warnings
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('zg.util.client')

class URLClient(object):
    #: List of (mimetype, binary-string) tuples
    magic = map(lambda (x, y): (x, y.decode('hex')), config('client.magic_numbers'))
    #: List of (mimetype, regexp)
    re_magic = map(lambda (x, y): (x, b'^'+y.replace(b'\x00', b'.')), magic)
    #: Size of the largest magic numbers string
    max_magic = max(map(lambda (x, y): len(y), magic))

    def __init__(self, url):
        self.url = url
        self.proxies = config('client.proxies')
        self.ua = config('client.user_agent')

        temp = config('client.temp')
        if not os.path.exists(temp):
            os.makedirs(temp)

    def discover(self):
        """
        Attempts to discover the content type of the url.
        """
        logger.info('discover attempt request url: ' + self.url)
        headers = {
                'User-Agent': self.ua,
                'Range': 'bytes=0-{}'.format(self.max_magic)
                }
        resp = requests.get(self.url, stream=True, verify=config('client.ssl_verify'),
                proxies=self.proxies, headers=headers)
        resp_type = resp.headers.get('content-type')
        resp_body = resp.raw.read(self.max_magic)
        resp.raw.close()
        logger.info('response type={} body={}'.format(resp_type, repr(resp_body)))

        magic = filter(lambda (x, y): re.match(y, resp_body), self.re_magic)
        if len(magic) > 0:
            logger.info('discovered type: {}'.format(magic[0][0]))
            return magic[0][0] # returns the mimetype

        else:
            pass

    def download(self):
        """
        Download the url to a temporary location.

        Creates a temporary file in config:client.temp
        """
        file, tempfile = mktemp()
        max_size = to_bytes(config('client.max_size'))
        chunk_size = to_bytes(config('client.chunk_size'))
        current_size = 0

        logger.info('download url: ' + self.url)
        try:
            resp = requests.get(self.url, stream=True, verify=config('client.ssl_verify'),
                    proxies=self.proxies, headers={'User-Agent': self.ua})
            if resp.status_code != 200:
                raise Exception('http code not ok')
            for chunk in resp.iter_content(chunk_size):
                current_size += len(chunk)
                if current_size > max_size:
                    raise Exception('download exceeded client.max_size')
                file.write(chunk)

        except Exception as e:
            logger.error(e)
            file.close()
            file = None
            os.remove(tempfile)
            tempfile = None

        if file:
            file.close()
            logger.info('download success, received {} with {}'.format(tempfile, format_bytes(current_size)))
        else:
            logger.error('download failure, response body size {}'.format(format_bytes(current_size)))

        return tempfile

