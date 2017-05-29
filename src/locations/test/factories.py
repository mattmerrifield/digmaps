from factory import DjangoModelFactory
from src.locations.models import Region


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region