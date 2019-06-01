from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django_extras import DjangoObjectType, DjangoFilterPaginateListField, DjangoSerializerMutation
from locations import models
import graphene

from locations.serializers import SiteSerializer


class SiteType(DjangoObjectType):
    class Meta:
        model = models.Site
        filter_fields = {
            "id": ["exact"],
            "code": ["exact", "icontains"],
            "region__id": ["exact"],
            "region__name": ["exact", "icontains"],
            "modern_name": ["icontains"],
            "ancient_name": ["icontains"],
            "area": ["lt", "gt"],
        }


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


