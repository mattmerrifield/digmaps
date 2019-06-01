import graphene
from django.contrib.gis.db.models import PointField
from graphene_django.converter import convert_django_field
from graphene_django_extras.converter import (
    convert_django_field as convert_django_field_extra,
)

__all__ = ["PointField", "PointFieldType"]


class PointFieldType(graphene.ObjectType):
    """
    An extremely simple representation of a single coordinate
    """

    x = graphene.Float()
    y = graphene.Float()


#################
# Register a GraphQL version of the PointField type we want to use
# This HAS to get imported somewhere before the SiteType is defined


@convert_django_field_extra.register(PointField)
@convert_django_field.register(PointField)
def convert_field_to_geojson(field, registry=None, *args, **kwargs):
    return graphene.Field(
        PointFieldType, description=field.help_text, required=not field.null
    )
