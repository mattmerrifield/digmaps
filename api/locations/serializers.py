import six
from django.contrib.gis.geos import GEOSException, GEOSGeometry
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import smart_str
from rest_framework import serializers
from rest_framework.utils import json
from django.utils.translation import gettext_lazy as _

from locations import models


class PointFieldSerializer(serializers.Field):
    """
    A field for handling GeoDjango Point fields as a json format.
    Expected input format:
        {
        "latitude": 49.8782482189424,
         "longitude": 24.452545489
        }
    """

    type_name = "PointField"
    type_label = "point"

    default_error_messages = {"invalid": _("Enter a valid location.")}

    def to_internal_value(self, value):
        """
        Parse json data and return a point object
        """
        if value in EMPTY_VALUES and not self.required:
            return None

        if isinstance(value, six.string_types):
            try:
                value = value.replace("'", '"')
                value = json.loads(value)
            except ValueError:
                self.fail("invalid")

        if value and isinstance(value, dict):
            try:
                latitude = value.get("latitude")
                longitude = value.get("longitude")
                return GEOSGeometry(
                    "POINT(%(longitude)s %(latitude)s)"
                    % {"longitude": longitude or None, "latitude": latitude or None}
                )
            except (GEOSException, ValueError):
                self.fail("invalid")
        self.fail("invalid")

    def to_representation(self, value):
        """
        Transform POINT object to json.
        """
        if value is None:
            return value

        if isinstance(value, GEOSGeometry):
            value = {"latitude": smart_str(value.y), "longitude": smart_str(value.x)}
        return value


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
