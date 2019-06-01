from graphene_django_extras import DjangoObjectType
import graphene


from graphene_django_extras import DjangoFilterPaginateListField
from locations import models as locations


class SiteType(DjangoObjectType):
    class Meta:
        model = locations.Site
        filter_fields = {
            "id": ["exact"],
            "code": ["exact", "icontains"],
            "region__id": ["exact"],
            "region__name": ["exact", "icontains"],
            "modern_name": ["icontains"],
            "ancient_name": ["icontains"],
            "area": ["lt", "gt"],
        }


class RegionType(DjangoObjectType):
    class Meta:
        model = locations.Region
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "description": ["icontains"],
        }


class FeatureType(DjangoObjectType):
    class Meta:
        model = locations.Feature


class PeriodType(DjangoObjectType):
    class Meta:
        model = locations.Period


class SiteFeatureType(DjangoObjectType):
    class Meta:
        model = locations.SiteFeature


class Query(graphene.ObjectType):
    """
    Start a top-level from one of the major models.
    """

    sites = DjangoFilterPaginateListField(SiteType)
    regions = DjangoFilterPaginateListField(RegionType)
    site_features = DjangoFilterPaginateListField(SiteFeatureType)
    features = DjangoFilterPaginateListField(FeatureType)



schema = graphene.Schema(query=Query)
