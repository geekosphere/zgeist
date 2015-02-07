"""
Zeitgeist Exceptions
"""

from __future__ import division, print_function, absolute_import, unicode_literals

class ZGError(Exception):
    pass

class ServiceError(ZGError):
    pass

class NotFound(ZGError):
    pass

