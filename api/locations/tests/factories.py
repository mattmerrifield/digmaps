from django.contrib.gis.geos import Point

from locations import models
import factory
from factory import faker


class RegionFactory(factory.DjangoModelFactory):
    name = faker.Faker('country')

    class Meta:
        model = models.Region


class SiteFactory(factory.DjangoModelFactory):
    code = factory.Sequence(lambda n: 'site_{}'.format(n))
    region = factory.RelatedFactory(RegionFactory)
    coordinates = factory.Sequence(lambda n: Point(n, n))

    class Meta:
        model = models.Site


class FeatureFactory(factory.DjangoModelFactory):
    shortname = factory.Sequence(lambda n: 'feature_{}'.format(n))

    class Meta:
        model = models.Feature


class PeriodFactory(factory.DjangoModelFactory):
    shortname = factory.Sequence(lambda n: 'period_{}'.format(n))
    start = factory.Sequence(lambda n: 100 * n - 3000)
    end = factory.Sequence(lambda n: 100 * n - 2900)

    class Meta:
        model = models.Period
