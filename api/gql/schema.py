from django_filters import FilterSet
from graphene_django_extras import (
    DjangoListObjectType,
    DjangoSerializerType,
    DjangoObjectType,
    DjangoFilterPaginateListField,
    DjangoListObjectField,
    DjangoFilterListField,
)
import graphene

from gql.objects import CoordinateType
from locations import models as locations
from locations import serializers


#################3
# Register the weird type we want to use
from django.contrib.gis.db.models import PointField
from graphene_django.converter import convert_django_field
from graphene_django_extras.converter import (
    convert_django_field as convert_django_field_extra,
)


@convert_django_field_extra.register(PointField)
@convert_django_field.register(PointField)
def convert_field_to_geojson(field, registry=None, *args, **kwargs):
    return graphene.Field(
        CoordinateType, description=field.help_text, required=not field.null
    )


class SiteType(DjangoSerializerType):
    class Meta:
        serializer_class = serializers.SiteSerializer
        filter_fields = {
            "id": ["exact"],
            "region__id": ["exact"],
            "region__name": ["exact", "icontains"],
            "modern_name": ["icontains"],
            "ancient_name": ["icontains"],
        }


class RegionType(DjangoSerializerType):
    class Meta:
        serializer_class = serializers.RegionSerializer


class FeatureType(DjangoSerializerType):
    class Meta:
        serializer_class = serializers.FeatureSerializer


class PeriodType(DjangoSerializerType):
    class Meta:
        serializer_class = serializers.PeriodSerializer


class SiteFeatureType(DjangoSerializerType):
    class Meta:
        serializer_class = serializers.SiteFeatureSerializer


class Query(graphene.ObjectType):
    """Start a top-level query somehow"""

    site = SiteType.RetrieveField()
    site_list = SiteType.ListField()

    region = RegionType.RetrieveField()
    region_list = RegionType.ListField()

    siteFeature = SiteFeatureType.RetrieveField()
    siteFeature_list = SiteFeatureType.ListField()

    feature = FeatureType.RetrieveField()
    feature_list = FeatureType.ListField()


schema = graphene.Schema(query=Query)
