from rest_framework import serializers
from gis_ext.serializers import PointFieldSerializer

from locations import models


class NestableModelSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        """
        We allow API users to pass in either a dictionary of data (like normal) or a single
        integer primary key for the model.

        For integers, we check if it's a valid primary key -- and if so, we'll return it as is.
        Otherwise, we'll do the usual deserialization conversion
        """
        plausible_pk = self.possible_pk(data)
        if plausible_pk and self.Meta.model.objects.filter(id=plausible_pk).exists():
            return data
        else:
            return super(NestableModelSerializer, self).to_internal_value(data)

    def possible_pk(self, data):
        if isinstance(data, int):
            return data
        elif isinstance(data, str) and all((i in "0123456789") for i in data):
            return int(data)
        else:
            return None


class FeatureSerializer(NestableModelSerializer):
    class Meta:
        model = models.Feature
        fields = ("id", "shortname", "name", "description")


class PeriodSerializer(NestableModelSerializer):
    class Meta:
        model = models.Period
        fields = ("id", "shortname", "name", "description", "start", "end")


class PeriodSummarySerializer(NestableModelSerializer):
    class Meta:
        model = models.Period
        fields = ("id", "shortname")


class FeatureSummarySerializer(NestableModelSerializer):
    class Meta:
        model = models.Feature
        fields = ("id", "shortname")


class RegionSummarySerializer(NestableModelSerializer):
    class Meta:
        model = models.Region
        fields = ("id", "shortname")


class RegionSerializer(NestableModelSerializer):
    class Meta:
        model = models.Region
        fields = ("name", "description")


class SiteFeatureSerializer(NestableModelSerializer):
    class Meta:
        model = models.SiteFeature
        depth = 2
        fields = ("site", "feature", "evidence", "periods")


class SiteSerializer(NestableModelSerializer):
    features = FeatureSummarySerializer(many=True, required=False, read_only=True)
    periods = PeriodSummarySerializer(many=True, required=False, read_only=True)
    coordinates = PointFieldSerializer()

    class Meta:
        model = models.Site
        depth = 2
        fields = (
            "id",
            "code",
            "modern_name",
            "ancient_name",
            "coordinates",
            "area",
            "population",
            "survey_type",
            "notes",
            "notes_easting_northing",
            "region",
            "references",
            "periods",
            "features",
            "periods",
            "features",
        )
