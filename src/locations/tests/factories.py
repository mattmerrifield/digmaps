from factory import DjangoModelFactory
from locations import models


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = models.Region


class SiteFactory(DjangoModelFactory):
    region = RegionFactory

    class Meta:
        model = models.Site


class FeatureFactory(DjangoModelFactory):
    class Meta:
        model = models.Feature


class PeriodFactory(DjangoModelFactory):
    class Meta:
        model = models.Period
