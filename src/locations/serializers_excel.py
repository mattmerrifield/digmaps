"""
Serializers to transform inbound records from an excel spreadsheet into
the denormalized version stored in the database
"""
import re

from rest_framework import serializers

from locations.models import Tag
from pprint import pprint
print = pprint


class TagField(serializers.CharField):
    """
    Some fields have text in them that indicates they should be tagged a certain way.
    """
    def __init__(self, **kwargs):
        kwargs['allow_blank'] = True
        kwargs['required'] = False
        super(TagField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """
        The text value is the field value.
        """
        print("Tag {} - {} - {}".format(self.field_name, self.label, data))
        return super(TagField, self).to_internal_value(data)


class PeriodField(serializers.NullBooleanField):
    """
    Check-boxes that indicate a site has artifacts from the given period.

    The field label is the field name
    """

    def __init__(self, **kwargs):
        kwargs['required'] = False
        super(PeriodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """
        The text value is the field value.
        """
        data = bool(data)
        return super(PeriodField, self).to_internal_value(data)


class RegionField(serializers.CharField):
    def to_internal_value(self, data):
        print("Region {}".format(data))
        return super(RegionField, self).to_internal_value(data)


class SiteSerializer(serializers.Serializer):
    """
    AutoID
    Site ID
    Modern Name
    Ancient Name
    Easting	Northing
    Easting-Long
    Northing-Lat
    SiteSize
    Region
    GeologicType
    SiteType
    SiteFunction
    BurialType
    Reference
    Notes
    Chalcolithic (undifferentiated)
    Early Chalcolithic
    Late Chalcolithic
    Early Bronze Age (undifferentiated)
    Early Bronze I
    Early Bronze II-III
    Early Bronze II
    Early Bronze III
    Early Bronze IV (undifferentiated)
    Early Bronze IVA
    Early Bronze IVB
    Early Bronze IVC
    Middle Bronze Age (undifferentiated)
    Middle Bronze I	Middle Bronze II-III
    Middle Bronze II
    Middle Bronze III
    Late Bronze Age (undifferentiated)
    Late Bronze I
    Late Bronze II
    Late Bronze III
    AutoID
    """
    AutoID = serializers.IntegerField()
    Site_ID = serializers.CharField()
    Modern_Name = serializers.CharField(required=False, allow_blank=True)
    Ancient_Name = serializers.CharField(required=False, allow_blank=True)
    Easting = serializers.FloatField(required=False, allow_null=True)
    Northing = serializers.FloatField(required=False, allow_null=True)
    Easting_Long = serializers.FloatField(required=False, allow_null=True)
    Northing_Lat = serializers.FloatField(required=False, allow_null=True)
    SiteSize = serializers.FloatField(required=False, allow_null=True)
    Region = RegionField(required=False)
    Reference = serializers.CharField(required=False, allow_null=True)
    Notes = serializers.CharField(required=False, allow_blank=True)

    # Freeform tags
    GeologicType = TagField()
    SiteType = TagField()
    SiteFunction = TagField()
    BurialType = TagField()

    # Time Period Tags
    Early_Bronze_IV = PeriodField()
    Late_Bronze_Age_undifferentiated = PeriodField()

    def to_internal_value(self, data):
        super(SiteSerializer, self).to_internal_value()



