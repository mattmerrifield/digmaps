from rest_framework import serializers
from locations import models


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
        fields = (
            'id',
            'shortname',
            'name',
            'description',
        )


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Period
        fields = (
            'id',
            'shortname',
            'name',
            'description',
            'start',
            'end',
        )


class SiteSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    periods = PeriodSerializer(many=True)

    class Meta:
        model = models.Site
        depth = 2
        fields = (
            'id',
            'code',
            'modern_name',
            'ancient_name',
            'coordinates',
            'area',
            'population',
            'survey_type',
            'notes',
            'notes_easting_northing',
            'region',
            'references',
            'features',
        )
