import graphene
from django.contrib.gis.db.models import PointField
from graphene_django.converter import convert_django_field

from gql.objects import CoordinateType


@convert_django_field.register(PointField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(
        CoordinateType, description=field.help_text, required=not field.null
    )
