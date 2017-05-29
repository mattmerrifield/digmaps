from django.test import TestCase

from src.locations.test.factories import RegionFactory


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

    def test_upwards_traversal(self):
        """
        A grand child can easily find the whole family tree
        """
        expected = [self.great1a_1, self.grand1a, self.child1, self.parent]
        observed = self.great1a_1.parents()
        self.assertEqual(expected, observed)

    def test_upwards_traversal_no_self(self):
        """
        Optionally, don't return the "self" region
        """
        expected = [self.grand1a, self.child1, self.parent]
        observed = self.great1a_1.parents(include_self=False)
        self.assertEqual(expected, observed)

    def test_downward_traversal(self):
        """
        A grand child can easily find the whole family tree
        """
        expected = [self.great1a_1, self.grand1a, self.child1, self.parent]
        observed = self.child1.sub_regions()
        self.assertEqual(expected, observed)

    def test_downwards_traversal_no_self(self):
        """
        Optionally, don't return the "self" region
        """
        expected = [self.great1a_1, self.great1a_2, self.grand1a, self.grand1b]
        observed = self.child1.sub_regions(include_self=False)
        self.assertEqual(expected, observed)

