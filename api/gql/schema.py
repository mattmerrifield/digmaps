from graphene_django import DjangoObjectType
import graphene
import graphql_geojson
from locations import models as locations
from bibliography import models as bibliography


class Region(DjangoObjectType):
    class Meta:
        model = locations.Region


class Site(graphql_geojson.GeoJSONType):
    class Meta:
        model = locations.Site
        geojson_field = 'coordinates'


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
    sites = graphene.List(Site)

    def resolve_users(self, info):
        return locations.Region.objects.all()


schema = graphene.Schema(query=Query)