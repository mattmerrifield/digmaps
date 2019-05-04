from django_filters import FilterSet
from graphene_django_extras import (
    DjangoListObjectType,
    DjangoSerializerType,
    DjangoObjectType,
    DjangoFilterPaginateListField,
)
from graphene_django import DjangoObjectType
import graphene

from gql.objects import CoordinateType
from locations import models as locations


#################3
# Register the weird type we want to use
from django.contrib.gis.db.models import PointField
from graphene_django.converter import convert_django_field


@convert_django_field.register(PointField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(
        CoordinateType, description=field.help_text, required=not field.null
    )


class Region(DjangoObjectType):
    class Meta:
        model = locations.Region


class SiteFilter(FilterSet):
    class Meta:
        fields = {
            "id": ['exact'],
            "region__name": ["exact", "icontains"],
            "modern_name": ["icontains"],
            "ancient_name": ["icontains"],
        }
        model = locations.Site


class Site(DjangoObjectType):
    class Meta:
        model = locations.Site


class Feature(DjangoObjectType):
    class Meta:
        model = locations.Feature


class Period(DjangoObjectType):
    class Meta:
        model = locations.Period


class SiteFeature(DjangoObjectType):
    class Meta:
        model = locations.SiteFeature


class Query(graphene.ObjectType):
    regions = graphene.List(Region)
    sites = DjangoFilterPaginateListField(
        Site,
        filterset_class=SiteFilter,
    )
    features = graphene.List(Feature)
    periods = graphene.List(Period)

    def resolve_regions(self, info):
        return locations.Region.objects.all()

    def resolve_features(self, info):
        return locations.Feature.objects.all()

    def resolve_periods(self, info):
        return locations.Period.objects.all()


schema = graphene.Schema(query=Query)
