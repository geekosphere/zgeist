
from __future__ import division, print_function, absolute_import, unicode_literals
from nose.tools import *
import os
from zg.util.client import URLClient
from zg.util import mktemp, md5file

def test_urlclient_discover():
    url = 'http://apoc.cc/test/img/'
    assert_equal('image/jpeg', URLClient(url+'test1.jpg').discover())
    assert_equal('image/png', URLClient(url+'test1.png').discover())
    assert_equal('image/gif', URLClient(url+'test2.gif').discover())
    assert_equal('image/bmp', URLClient(url+'test2.bmp').discover())
    assert_equal('image/webp', URLClient(url+'test2.webp').discover())
    assert_equal(None, URLClient(url).discover())

def test_urlclient_download():
    tempfile = URLClient('http://apoc.cc/test/img/test1.jpg').download()
    assert(os.path.isfile(tempfile))
    assert_equal('82fc99869780f46d681e80b517b22234', md5file(tempfile))
    os.remove(tempfile)
    # 404 code:
    assert(not URLClient('http://apoc.cc/does-not-exist').download())
    assert(not URLClient('http://doesnt-exist.fugtld/foo.jpg').download())
    # test config sets max_size to 1MiB, here we test
    #    that too large files are rejected:
    assert(not URLClient('http://apoc.cc/test/2MiBfile').download())
    # should allow invalid SSL:
    tempfile = URLClient('https://apoc.cc/test/img/test1.jpg').download()
    assert(tempfile)
    os.remove(tempfile)

