"""
Service Base
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from .event import Event, EventRegistry
from zg.database import session
from zg.util import utcnow
from zg.error import NotFound
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class Service(object):

    class event(EventRegistry):
        """Default service events emitted when the persistent data changes."""
        #: Called when a new model was created.
        created = Event()
        #: Called when model attributes change or update() was invoked.
        updated = Event()
        #: Called when the model gets removed.
        deleted = Event()

    def __init__(self, model):
        """Initialize a new service instance for the specified model."""
        if model.__class__ != self.__model__:
            raise ServiceError('wrong model initializer')
        self.model = model

    def __getattr__(self, name):
        """Delegates getting an attribute on the model instance."""
        return getattr(self.model, name)

    def count(cls):
        """Return number of all objects in the database."""
        return cls.query().count()

    def delete(self):
        """Removes a object from the database."""
        session.query(self.__model__).filter_by(id=self.id).delete()
        session.commit()
        self.event.deleted.publish(self.id)
        self.model = None

    def update(self, **kwargs):
        """Updates the object model and persists changes in the database."""
        kwargs['updated_at'] = utcnow()
        session.query(self.__model__).filter_by(id=self.id).update(kwargs)
        session.commit()
        self.event.updated.publish(self)

    @classmethod
    def query(cls):
        """Returns the query for the object."""
        return session.query(cls.__model__)

    @classmethod
    def one(cls, query):
        """Given a query object return one result or raises NotFound."""
        try:
            model = query.one()
        except (NoResultFound, MultipleResultsFound):
            raise NotFound('No {} result found'.format(cls.__name__))
        return cls(model)

    @classmethod
    def all(cls, query):
        """Given a query object return results as a list (or empty list)."""
        return map(cls, query.all())

    @classmethod
    def get(cls, id):
        """Queries a object by id."""
        return cls.one(cls.query().filter_by(id=id))

    @classmethod
    def find_one(cls, **criteria):
        """Queries a object by filter_by criteria."""
        return cls.one(cls.query().filter_by(**criteria))

    @classmethod
    def find_by_id(cls, id):
        """Queries a object by id."""
        return cls.get(id)

    @classmethod
    def find_all(cls):
        """Queries all objects."""
        return cls.all(cls.query())

    @classmethod
    def find_or_create(cls, **criteria):
        """Finds or creates a object by criteria."""
        try:
            return cls.find_one(**criteria)
        except NotFound:
            return cls.create(**criteria)

    @classmethod
    def create(cls, **kwargs):
        """Creates a new object with a model attached to it."""
        model = cls.__model__(**kwargs)
        model.created_at = utcnow()
        service = cls(model)

        session.add(model)
        session.commit()
        cls.event.created.publish(service)

        return service

class ManyMapping(object):
    def __init__(self, obj, service=None, collection=None):
        self._obj = obj
        self._service = service if service else self.__class__.__service__
        self._collection = collection if collection else self.__class__.__collection__

    def collection(self):
        return getattr(self._obj.model, self._collection)

    def __len__(self):
        return len(self.collection())

    def __contains__(self, item):
        return item.model in self.collection()

    def __iter__(self):
        for item in map(self._service, self.collection()):
            yield item

    def append(self, item):
        self.assign(item)

    def assign(self, item):
        self.collection().append(item.model)
        self._service.event.assigned.publish(self._obj, item)

    def remove(self, item):
        self.unassign(item)

    def unassign(self, item):
        self.collection().remove(item.model)
        self._service.event.unassigned.publish(self._obj, item)



