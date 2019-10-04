from django.db import models
from gis_ext.fields import (
    PointField,
)  # Like django.contrib.gis.db.models.PointField, but with GQL support
from locations.constants import Evidence

from .constants import Survey


class Region(models.Model):
    """
    A general geographical area.
    """

    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{} {}".format(self.pk, self.name)


class Site(models.Model):
    """
    An archaeological site.
    """

    code = models.CharField(
        max_length=40,
        null=False,
        help_text="Short, meaningful identifier for the site. Assigned by the admin.",
    )
    modern_name = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default='',
        help_text="Name used by modern peoples",
    )
    ancient_name = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default='',
        help_text="Name used by ancient peoples to describe the location",
    )
    coordinates = PointField(null=False, blank=False)
    area = models.FloatField(
        null=True,
        blank=True,
        help_text="Area of the site in Hectares. Null represents 'unknown'"
    )
    population = models.FloatField(null=True, blank=True)
    survey_type = models.CharField(
        null=False,
        blank=True,
        default="",
        choices=Survey.choices(), max_length=25
    )
    notes = models.TextField(blank=True, default="", null=False)
    notes_easting_northing = models.TextField(
        blank=True,
        null=False,
        editable=False,
        default="",
        help_text="value of the original coordinate system of record, if it was easting/northing. Do not use directly",
    )
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    references = models.ManyToManyField("bibliography.Publication")
    features = models.ManyToManyField(
        "Feature", related_name="sites", through="SiteFeature"
    )
    periods = models.ManyToManyField(
        "Period", related_name="sites", through="SitePeriod"
    )


class Feature(models.Model):
    """
    Important characteristics of an archaeological site

    Examples:
        - Tel
        - Fortification
        - Carin Burial
    """

    shortname = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(default="")


class Period(models.Model):
    """
    An archaeological period, e.g. "Early Bronze Age"

    When attached to a Site, indicates occupation of that site during that time

    When attached to a Feature, indicates presence of that feature during
    that time
    """

    name = models.CharField(max_length=50)
    shortname = models.CharField(
        max_length=10, unique=True, help_text="Unique code name, e.g. 'EBIV'"
    )
    description = models.TextField(default="")
    start = models.IntegerField(help_text="Approximate Beginning (BCE is negative)")
    end = models.IntegerField(help_text="Approximate Ending (BCE is negative)")

    def __str__(self):
        return self.shortname


class SiteFeature(models.Model):
    """
    Tag a site with a feature. Optionally, specify the period(s) for which the
    tag is valid.
    """

    class Meta:
        unique_together = ("site", "feature")

    site = models.ForeignKey("Site", on_delete=models.CASCADE)
    feature = models.ForeignKey("Feature", on_delete=models.CASCADE)
    evidence = models.PositiveSmallIntegerField(
        default=Evidence.TYPICAL.value,
        choices=Evidence.choices(),
        help_text="How clear is the evidence for the site to have this feature?",
    )
    periods = models.ManyToManyField("Period")


class SitePeriod(models.Model):
    """
    Vanilla through-model
    """

    site = models.ForeignKey("Site", on_delete=models.CASCADE)
    period = models.ForeignKey("Period", on_delete=models.CASCADE)
