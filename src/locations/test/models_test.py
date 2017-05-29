from django.test import TestCase


class RegionTest(TestCase):
    """
    Test the functionality of the recursive parent/child relationship that
    Region objects will store.
    """
    def setUpTestData(cls):
        cls.parent = RegionFactory()

        cls.child1 = RegionFactory(parent=cls.parent)
        cls.child2 = RegionFactory(parent=cls.parent)

        cls.grand1a = RegionFactory(parent=cls.child1)
        cls.grand1b = RegionFactory(parent=cls.child1)
        cls.grand2a = RegionFactory(parent=cls.child2)
        cls.grand2b = RegionFactory(parent=cls.child2)

        cls.great1a_1 = RegionFactory(parent=cls.grand1a)
        cls.great1a_2 = RegionFactory(parent=cls.grand1a)
