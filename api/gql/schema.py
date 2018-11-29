from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
import graphene
from locations import models as locations
from bibliography import models as bibliography
from django.contrib.gis.db.models import PointField


class PointType(graphene.ObjectType):
    """
    Very simple GeoJSON representation for a PointField
    """
    type = graphene.String()
    coordinates = graphene.List(graphene.Float)

    def resolve_type(self, info):
        """
        A point is.... always a point. Duh.
        """
        return "point"

    def resolve_coordinates(self, info):
        return info.x, info.y


@convert_django_field.register(PointField)
def convert_point_field(field, registry=None):
    return PointType()


class Region(DjangoObjectType):
    class Meta:
        model = locations.Region


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
    sites = graphene.List(Site, id=graphene.ID())
    features = graphene.List(Feature)
    periods = graphene.List(Period)

    def resolve_regions(self, info):
        return locations.Region.objects.all()

    def resolve_sites(self, info, id):
        return locations.Site.objects.filter(id=id)

    def resolve_features(self, info):
        return locations.Feature.objects.all()

    def resolve_periods(self, info):
        return locations.Period.objects.all()


schema = graphene.Schema(query=Query)