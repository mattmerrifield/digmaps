import graphene
from django.contrib.gis.db.models import PointField
from graphene_django_extras.converter import convert_django_field




class CoordinateType(graphene.ObjectType):
    """
    An extremely simple representation of a single coordinate
    """

    x = graphene.Float()
    y = graphene.Float()


@convert_django_field.register(PointField)
def convert_field_to_geojson(field, registry=None):
    return graphene.Field(
        CoordinateType, description=field.help_text, required=not field.null
    )
