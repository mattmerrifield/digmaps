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
    modern_name = models.CharField(max_length=50, blank=True, help_text="Name used by modern peoples")
    ancient_name = models.CharField(max_length=50, blank=True, help_text="Name used by ancient peoples")
    coordinates = PointField()
    area = models.FloatField(null=True, blank=True, help_text="Area in Hectares. Null is 'unknown'")
    survey_type = models.CharField(blank=True, default="", choices=SURVEY_CHOICES, max_length=25)
    notes = models.TextField(blank=True, default="")
    notes_easting_northing = models.TextField(
        blank=True, default='',
        help_text="value of the original coordinate system of record, if it was easting/northing. Do not use directly"
    )
    region = models.ForeignKey(Region, null=True)
    references = models.ManyToManyField('bibliography.Publication')
    features = models.ManyToManyField('Feature', through='SiteFeature')


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

    shortname = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    sites = models.ManyToManyField('Site', related_name='tags', through='SiteFeature')


class SiteFeature(models.Model):
    """
    Tag a site with a feature. Optionally, specify the period(s) for which the
    tag is valid.
    """
    class Meta:
        unique_together = ('site', 'feature')

    site = models.ForeignKey('Site')
    feature = models.ForeignKey('Feature')
    evidence = models.IntegerField(
        default=Evidence.TYPICAL, choices=Evidence.CHOICES,
        help_text="How clear is the evidence for the site to have this feature?"
    )
    periods = models.ManyToManyField('Period')


class SitePeriod(models.Model):
    """
    Vanilla through-model
    """
    site = models.ForeignKey('Site')
    period = models.ForeignKey('Period')


class Period(models.Model):
    """
    An archaeological period, e.g. "Early Bronze Age"

    When attached to a Site, indicates occupation of that site during that time

    When attached to a Feature, indicates presence of that feature during
    that time
    """
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=10, unique=True, help_text="Unique code name, e.g. 'EBIV'")
    description = models.TextField(default='')
    start = models.IntegerField(help_text="Approximate Beginning (BCE is negative)")
    end = models.IntegerField(help_text="Approximate Ending (BCE is negative)")

    sites = models.ManyToManyField(Site, related_name='occupation_periods', through='SitePeriod')

    def __str__(self):
        return self.shortname

