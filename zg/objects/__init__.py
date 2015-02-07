"""
Object Package Title
~~~~~~~~~~~~~~~~~~~~

The package automatically exposes the public services API::

   from zg.objects import Item

Services wrap data objects (sqlalchemy models), provide customized
type specific business logic combined with a common service API.
The main reasoning behind going to all this trouble wrapping
the models is to ovoid overly fat model classes (models only declare
data nothing else), aswell as to publish object events.
"""

from zg.util import environment

from .item.service import Item
from .tag.service import Tag

