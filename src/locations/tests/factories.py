from factory import DjangoModelFactory
from locations.models import Region


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region