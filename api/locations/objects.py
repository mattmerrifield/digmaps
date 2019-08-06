from django.contrib.gis.forms.fields import GeometryField
from django.contrib.gis.geos import GEOSGeometry
from django.forms import CharField
from django_filters.rest_framework import FilterSet, BooleanFilter, CharFilter, Filter
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django_extras import DjangoObjectType, DjangoFilterPaginateListField, DjangoSerializerMutation
from graphql_geojson import Geometry

from locations import models
import graphene

from locations.serializers import SiteSerializer


class GeometryFilter(Filter):
    field_class = CharField


class SiteFilterset(FilterSet):
    """Filter for Books by if books are published or not"""
    within = GeometryFilter(field_name='coordinates', method='filter_within')
    rect = GeometryFilter(field_name='coordinates', method='filter_rect')

    def filter_rect(self, queryset, name, value):
        # Shorthand for a WKT for a rectangle
        x1, y1, x2, y2 = value.replace("(", "").replace(")", "").split(",")
        # construct the full lookup expression.
        rectangle = GEOSGeometry(f'POLYGON (({x1} {y1}, {x1} {y2}, {x2} {y2}, {x2} {y1}, {x1} {y1}))')
        lookup = '{}__within'.format(name)
        return queryset.filter(**{lookup: rectangle})

    def filter_within(self, queryset, name, value):
        # construct the full lookup expression. from a WKT string
        shape = GEOSGeometry(value)
        lookup = '{}__within'.format(name)
        return queryset.filter(**{lookup: shape})

    class Meta:
        model = models.Site
        filter_overrides = {
            models.PointField: {
                'filter_class': GeometryFilter,
                'extra': lambda f: {
                    'lookup_expr': 'rect',
                },
            },
        }
        fields = [
            'id', 'code', 'region', 'region__name', 'within', 'rect'
        ]


class SiteType(DjangoObjectType):
    class Meta:
        model = models.Site
        filterset_class = SiteFilterset



class RegionType(DjangoObjectType):
    class Meta:
        model = models.Region
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "description": ["icontains"],
        }


class FeatureType(DjangoObjectType):
    class Meta:
        model = models.Feature


class PeriodType(DjangoObjectType):
    class Meta:
        model = models.Period


class SiteFeatureType(DjangoObjectType):
    class Meta:
        model = models.SiteFeature


class Query(graphene.ObjectType):
    """
    Start a top-level from one of the major models.
    """
    sites = DjangoFilterPaginateListField(SiteType)
    regions = DjangoFilterPaginateListField(RegionType)
    site_features = DjangoFilterPaginateListField(SiteFeatureType)
    features = DjangoFilterPaginateListField(FeatureType)


class SiteSerializerMutation(DjangoSerializerMutation):
    class Meta:
        serializer_class = SiteSerializer
        # model_operations = ['create', 'update']
        # lookup_field = 'id'


class Derp(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, name):
        print("derp")


class Mutation(graphene.ObjectType):
    """
    Create & Update operations for the DB models, mediated by the locations.
    """
    derp = Derp.Field()

    # site = SiteSerializerMutation.Field()
    # update_site = SiteSerializerMutation.UpdateField()
    # create_field = SiteSerializerMutation.CreateField()

    # create_region = RegionType.CreateField()
    # update_region = RegionType.UpdateField()
    #
    # create_feature = FeatureType.CreateField()
    # update_feature = FeatureType.UpdateField()
    #
    # create_site_feature = SiteFeatureType.CreateField()
    # update_site_feature = SiteFeatureType.UpdateField()


