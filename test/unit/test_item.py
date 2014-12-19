
from unittest import TestCase

from zgeist.model import Item

class ItemUnitTest(TestCase):

    def test_query(self):
        assert Item.query.count() == 0


