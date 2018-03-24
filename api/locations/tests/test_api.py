from rest_framework import test

from locations import models
from locations.tests import factories


class APITestCase(test.APITestCase):
    """
    The region endpoint is the simplest, supporting only the standard actions, and containing
    no nested data.
    
    We'll use it as a base
    """
    factory = factories.RegionFactory
    model = models.Region
    endpoint = "regions"

    CREATE = {
        'name': 'New Region',
        'description': 'A land of new opportunities.',
    }

    PARTIAL_UPDATE = {
        'description': 'We have updated the description field here',
    }

    @classmethod
    def setUpTestData(cls):
        super(APITestCase, cls).setUpTestData()
        cls.object_1 = cls.factory()
        cls.object_2 = cls.factory()

    def setUp(self):
        super(APITestCase, self).setUp()
        self.assertEqual(2, self.model.objects.count())

    def test_retrieve(self):
        """
        You may request a specific region by its ID
        """
        response = self.client.get('/{}/{}/'.format(self.endpoint, self.object_1.id))
        self.assertEqual(200, response.status_code)

    def test_list(self):
        """
        A plain GET To the regions endpoint returns a paginated list of regions
        """
        response = self.client.get('/{}/'.format(self.endpoint))
        self.assertEqual(200, response.status_code)

    def test_create(self):
        """
        You may POST some JSON to create a new region
        """
        response = self.client.post('/{}/'.format(self.endpoint), data=self.CREATE, format='json')
        self.assertEqual(201, response.status_code)  # 201 - Created
        self.assertEqual(3, self.model.objects.count())

    def test_delete(self):
        """
        You may delete a region. Doing so will remove it from the database, but will NOT delete the associated sites.
        """
        self.assertEqual(2, self.model.objects.count())
        response = self.client.delete('/{}/{}/'.format(self.endpoint, self.object_2.id))
        self.assertEqual(204, response.status_code)
        self.assertEqual(1, self.model.objects.count())

    def test_partial_update(self):
        old_attributes = {}
        # Save all the original attributes for later comparison
        for key in self.PARTIAL_UPDATE.keys():
            old_attributes[key] = getattr(self.object_2, key)

        # Make sure we're actually trying to change something, or this test will be meaningless
        self.assertNotEquals(old_attributes, self.PARTIAL_UPDATE)
        self.assertTrue(len(self.PARTIAL_UPDATE) >=1)
        # Partially update the attributes using the API
        response = self.client.patch('/{}/{}/'.format(self.endpoint, self.object_2.id), data=self.PARTIAL_UPDATE, format='json')
        self.assertEqual(200, response.status_code)
        self.object_2.refresh_from_db()

        # Pull the new attributes and compare
        new_attributes = {}
        for key in self.PARTIAL_UPDATE.keys():
            new_attributes[key] = getattr(self.object_2, key)
        self.assertEqual(new_attributes, self.PARTIAL_UPDATE)


class SiteEndpointTests(APITestCase):
    """
    The Site endpoint supports the standard actions.
    """
    factory = factories.SiteFactory
    model = models.Site
    endpoint = "sites"

    CREATE = {
        # These are the only fields which are strictly required. The rest can be blank.
        'code': 'abcd1234',
        'coordinates': {
            'latitude': 123,
            'longitude': 321,
        },
    }
    PARTIAL_UPDATE = {
        # Pick any field at random, really. This is just a spot check.
        'survey_type': 'surface',
    }


class PeriodEndpointTests(APITestCase):
    """
    The Period endpoint supports the standard actions.
    """
    factory = factories.PeriodFactory
    model = models.Period
    endpoint = "periods"

    CREATE = {
        # These are the only fields which are strictly required. The rest can be blank.
        'shortname': 'SA',
        'name': 'The Space Age',
        'description': 'Rockets & Russians & stuff',
        'start': 1957,  # The Russians are gonna get us!
        'end': 1969,    # One small step for man...
    }
    PARTIAL_UPDATE = {
        # Pick any field at random, really. This is just a spot check.
        'description': 'spaaaaaaaace',
    }


class FeatureEndpointTests(APITestCase):
    """
    The Feature endpoint supports the standard actions.
    """
    factory = factories.FeatureFactory
    model = models.Feature
    endpoint = "features"

    CREATE = {
        # These are the only fields which are strictly required. The rest can be blank.
        'name': 'Small Mounds',
        'shortname': 'mounds',
        'description': 'Don\'t make a mountain out of them',
    }

    PARTIAL_UPDATE = {
        # Pick any field at random, really. This is just a spot check.
        'description': 'Actually, let\'s make a mountain out of them after all!',
    }
