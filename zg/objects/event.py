"""
Service PubSub Event
"""

from __future__ import division, print_function, absolute_import, unicode_literals
import inspect

class EventRecorder(object):
    def __init__(self, event):
        self.recording = []
        self._event = event

    def consumer(self, *args):
        self.recording.append(args)

    def __contains__(self, item):
        return item in self.recording

    def __enter__(self):
        self._event.subscribe(self.consumer)

    def __exit__(self, type, value, traceback):
        self._event.unsubscribe(self.consumer)

class Event(object):

    def __init__(self):
        self._subscribers = []

    def publish(self, *args):
        map(lambda f: f(*args), self._subscribers)

    def subscribe(self, func):
        self._subscribers.append(func)

    def unsubscribe(self, func):
        self._subscribers.remove(func)

class EventRegistry(object):
    """Event PubSub for Services."""
    @classmethod
    def subscribe(cls, func):
        """Subscribes to all events of this registry."""
        def func_wrapper(name, func):
            def wrapper(*args):
                return func(name, *args)
            return wrapper
        events = inspect.getmembers(cls, lambda a:not(inspect.isroutine(a)))
        for name, event in events:
            if not(name.startswith('__') and name.endswith('__')):
                event.subscribe(func_wrapper(name, func))


