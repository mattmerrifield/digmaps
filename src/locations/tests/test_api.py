from rest_framework import test

from locations import models
from locations.tests import factories


class APITestCase(test.APITestCase):
    """
    Instructive examples about how to use the API
    """


class RegionEndpointTests(APITestCase):
    """
    The region endpoint supports the standard actions.
    """
    @classmethod
    def setUpTestData(cls):
        cls.region_1 = factories.RegionFactory()
        cls.region_2 = factories.RegionFactory()

    def setUp(self):
        super(RegionEndpointTests, self).setUp()
        self.assertEqual(2, models.Region.objects.count())

    ######
    # Simple operations
    def test_list_regions(self):
        """
        A plain GET To the regions endpoint returns a paginated list of regions
        """
        response = self.client.get('/api/v1/regions/')
        print(response)
        self.assertEqual(200, response.status_code)

    def test_get_region(self):
        """
        You may request a specific region by its ID
        """
        response = self.client.get('/api/v1/regions/{}/'.format(self.region_1.id))
        print(response)
        self.assertEqual(200, response.status_code)

    def test_create_region(self):
        """
        You may POST some JSON to create a new region
        """
        response = self.client.post('/api/v1/regions/', data={
            'name': 'New Region',
            'description': 'A land of new opportunities.',
        })
        print(response)
        self.assertEqual(201, response.status_code)  # 201 - Created
        self.assertEqual(3, models.Region.objects.count())

    def test_delete_region(self):
        """
        You may delete a region. Doing so will remove it from the database, but will NOT delete the associated sites.
        """
        self.assertEqual(2, models.Region.objects.count())
        response = self.client.delete('/api/v1/regions/{}/'.format(self.region_2.id))
        print(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, models.Region.objects.count())

    def test_partial_update_region(self):
        old_text = self.region_2.description
        response = self.client.patch('/api/v1/regions/{}/'.format(self.region_2.id), data={
            'description': 'We have updated the description field here',
        })
        print(response)
        self.assertEqual(200, response.status_code)
        self.region_2.refresh_from_db()
        new_text = self.region_2.description
        self.assertNotEquals(old_text, new_text)
        self.assertEqual(new_text, 'We have updated the description field here')
