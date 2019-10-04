from django.contrib.gis.geos import GEOSGeometry
from django.forms import CharField
from django_filters.rest_framework import FilterSet, Filter
from graphene import Argument, ID
from graphene_django.filter.utils import get_filtering_args_from_filterset
from graphene_django_extras import DjangoObjectType, DjangoFilterPaginateListField, DjangoSerializerMutation
import graphene as g
from graphene_django_extras.filters.filter import get_filterset_class
from graphene_django_extras.paginations.pagination import BaseDjangoGraphqlPagination
from graphene_django_extras.settings import graphql_api_settings

from locations import models
import graphene

from locations.serializers import SiteSerializer


class GeometryFilter(Filter):
    field_class = CharField


class SiteFilterset(FilterSet):
    """
    Filter for Sites based on WKT geometry
    """
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
    # We have to (unfortunately) explicitly list out field types for the non-null fields
    id = g.NonNull(g.ID)
    code = g.NonNull(g.String)
    modern_name = g.NonNull(g.String)
    ancient_name = g.NonNull(g.String)
    area = g.NonNull(g.Float)
    population = g.NonNull(g.Float)
    survey_type = g.NonNull(g.String)

    class Meta:
        model = models.Site
        filterset_class = SiteFilterset


class RegionType(DjangoObjectType):
    name = g.NonNull(g.String)
    description = g.NonNull(g.String)

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



class ListFieldHowItShouldHaveBeenAllAlong(DjangoFilterPaginateListField):

    def __init__(self, _type, pagination=None, fields=None, extra_filter_meta=None,
                 filterset_class=None, *args, **kwargs):

        _fields = _type._meta.filter_fields
        _model = _type._meta.model

        self.fields = fields or _fields
        meta = dict(model=_model, fields=self.fields)
        if extra_filter_meta:
            meta.update(extra_filter_meta)

        filterset_class = filterset_class or _type._meta.filterset_class
        self.filterset_class = get_filterset_class(filterset_class, **meta)
        self.filtering_args = get_filtering_args_from_filterset(self.filterset_class, _type)
        kwargs.setdefault('args', {})
        kwargs['args'].update(self.filtering_args)

        if 'id' not in kwargs['args'].keys():
            self.filtering_args.update({'id': Argument(ID, description='Django object unique identification field')})
            kwargs['args'].update({'id': Argument(ID, description='Django object unique identification field')})

        pagination = pagination or graphql_api_settings.DEFAULT_PAGINATION_CLASS()

        if pagination is not None:
            assert isinstance(pagination, BaseDjangoGraphqlPagination), (
                'You need to pass a valid DjangoGraphqlPagination in DjangoFilterPaginateListField, received "{}".'
            ).format(pagination)

            pagination_kwargs = pagination.to_graphql_fields()

            self.pagination = pagination
            kwargs.update(**pagination_kwargs)

        if not kwargs.get('description', None):
            kwargs['description'] = '{} list'.format(_type._meta.model.__name__)

        # Intention super skip. Ew
        super(DjangoFilterPaginateListField, self).__init__(g.NonNull(g.List(g.NonNull(_type))), *args, **kwargs)



class Query(graphene.ObjectType):
    """
    Start a top-level from one of the major models.
    """
    sites = ListFieldHowItShouldHaveBeenAllAlong(SiteType)
    regions = ListFieldHowItShouldHaveBeenAllAlong(RegionType)
    site_features = ListFieldHowItShouldHaveBeenAllAlong(SiteFeatureType)
    features = ListFieldHowItShouldHaveBeenAllAlong(FeatureType)


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


