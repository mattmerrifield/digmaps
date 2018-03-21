from django.db import models
from django.contrib.gis.db.models import PointField
from digmaps.constants import Evidence


class Region(models.Model):
    """
    A general geographical area.

    Can be nested. Be cautious when making queries for sites in a given region
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{} {}".format(self.pk, self.name)


class Site(models.Model):
    """
    An archaeological site.
    """
    SURVEY_CHOICES = (
        ('surface', 'Surface Survey'),
        ('excavation', 'Excavation'),
    )

    code = models.CharField(max_length=24, help_text="Short, meaningful ID for the site. Assigned by the admin")
    modern_name = models.CharField(max_length=50, null=True, blank=True, help_text="Name used by modern peoples")
    ancient_name = models.CharField(max_length=50, null=True, blank=True, help_text="Name used by ancient peoples")
    coordinates = PointField()
    area = models.FloatField(null=True, blank=True, help_text="Area in Hectares")
    survey_type = models.CharField(default="", choices=SURVEY_CHOICES)
    notes = models.TextField(default="")
    notes_easting_northing = models.TextField(
        help_text="The original coordinate system of record. "
                  "This value has been projected into lat/lon,"
                  " and should not be used directly.")
    region = models.ForeignKey(Region, null=True, blank=True)
    references = models.ManyToManyField('bibliography.Publication')
    features = models.ForeignKey('Feature', through='SiteFeature')


class Feature(models.Model):
    """
    Important characteristics of an archaeological site

    Examples:
        - Tel
        - Fortification
        - Carin Burial
    """

    TOMB = 'tomb'
    CARIN = 'carin'
    CEMETARY = 'cemetary'

    BURIAL_TYPES = [
        (TOMB, 'Tomb'),
        (CARIN, 'Carins'),
        (CEMETARY, 'Cemetary'),
    ]

    shortname = models.CharField(max_length=10, unique=True)  # e.g. EBIV
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    sites = models.ManyToManyField(
        Site, related_name='tags', through='SiteFeatureTag'
    )


class SiteFeature(models.Model):
    """
    Tag a site with a feature. Optionally, specify the period(s) for which the
    tag is valid.
    """
    class Meta:
        unique_together = ('site', 'tag')

    site = models.ForeignKey('Site')
    feature = models.ForeignKey('Tag')
    evidence = models.IntegerField(
        null=True, blank=True, choices=Evidence.CHOICES, max_length=24,
        help_text="How clear is the evidence for the site to have this tag?"
    )
    periods = models.ManyToManyField('Period')


class Period(models.Model):
    """
    An archaeological period, e.g. "Early Bronze Age"

    When attached to a Site, indicates occupation of that site during that time

    When attached to a Feature, indicates presence of that feature during
    that time
    """
    shortname = models.CharField(max_length=10, unique=True)  # e.g. EBIV
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    sites = models.ManyToManyField(
        Site, related_name='occupation', through='SitePeriod'
    )
    start = models.IntegerField(
        help_text="Approximate Beginning (BCE is negative)")
    end = models.IntegerField(
        help_text="Approximate Ending (BCE is negative)")

    parent = models.ForeignKey("self")

    def __str__(self):
        return self.shortname

