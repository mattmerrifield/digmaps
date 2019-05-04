from django_filters import FilterSet
from graphene_django_extras import (
    DjangoListObjectType,
    DjangoSerializerType,
    DjangoObjectType,
    DjangoFilterPaginateListField,
    DjangoListObjectField, DjangoFilterListField)
import graphene

from gql.objects import CoordinateType
from locations import models as locations


#################3
# Register the weird type we want to use
from django.contrib.gis.db.models import PointField
from graphene_django.converter import convert_django_field
from graphene_django_extras.converter import convert_django_field as convert_django_field_extra


@convert_django_field_extra.register(PointField)
@convert_django_field.register(PointField)
def convert_field_to_geojson(field, registry=None, *args, **kwargs):
    return graphene.Field(
        CoordinateType, description=field.help_text, required=not field.null
    )


class Region(DjangoObjectType):
    class Meta:
        model = locations.Region


class SiteListType(DjangoObjectType):
    class Meta:
        model = locations.Site
        filter_fields = {
            "id": ['exact'],
            "region__id": ['exact',],
            "region__name": ["exact", "icontains"],
            "modern_name": ["icontains"],
            "ancient_name": ["icontains"],
        }


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
    regions = DjangoFilterListField(Region)
    sites = DjangoFilterListField(SiteListType)
    features = DjangoFilterListField(Feature)
    periods = DjangoFilterListField(Period)


schema = graphene.Schema(query=Query)
