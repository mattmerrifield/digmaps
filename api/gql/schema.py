from graphene_django import DjangoObjectType
import graphene

from locations import models as locations


class Region(DjangoObjectType):
    class Meta:
        model = locations.Region


class Site(DjangoObjectType):
    class Meta:
        filter_fields = {
            "region__name": ["exact", "icontains"],
            "modern_name": ["icontains"],
            "ancient_name": ["icontains"],
        }
        model = locations.Site
        interfaces = (graphene.relay.Node,)


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
    sites = graphene.List(
        Site,
        id=graphene.ID(),
        modern_name=graphene.String(),
        ancient_name=graphene.String(),
    )
    features = graphene.List(Feature)
    periods = graphene.List(Period)

    def resolve_sites(self, info, id=None, modern_name=None, ancient_name=None):
        return locations.Site.objects.all()

    def resolve_regions(self, info):
        return locations.Region.objects.all()

    def resolve_features(self, info):
        return locations.Feature.objects.all()

    def resolve_periods(self, info):
        return locations.Period.objects.all()


schema = graphene.Schema(query=Query)
