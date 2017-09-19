from django.db import models
from django.contrib.gis.db.models import PointField
from digmaps.constants import Evidence

class RecursiveModelQuerySet(models.QuerySet):
    """Provides convenience methods for querying with .parents() and
    .children()"""
    def has_parent(self, obj):
        """
        Returns all objects which are a direct descendant of the given object.
        """
        parents = obj.parents(include_self=False)
        return self.filter(pk__in=[p.pk for p in parents])

    def has_descendant(self, obj):
        """
        Returns all objects which have the given one somewhere below them in
        their tree.
        """
        children = obj.children
        return self.filter(pk__in=[c.pk for c in children])


class RecursiveModel(models.Model):
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name='immediate_children'
    )

    objects = RecursiveModelQuerySet.as_manager()

    class Meta:
        abstract = True

    def parents(self, include_self=True, depth=None):
        """
        Returns a list like:

          [parent, grandparent, great-grandparent, ..., (great)^n-grandparent]

        describing the 'ancestors' of this recursively-associated model.
        """
        ancestors = [self] if include_self else []
        parent = self.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

    def children(self, include_self=True):
        """
        Returns a list of all children, all grandchildren, all
        great-grandchildren, etc.
        """
        family = []
        for r in self.children.all():
            family.extend(r.child_regions())
        if include_self:
            family.append(
                self)  # Parent goes last, to follow recursion pattern
        return family


class Region(RecursiveModel):
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

    code = models.CharField(
        max_length=24,
        help_text="Short, meaningful ID for the site. Assigned by the admin")
    modern_name = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="Name commonly used by modern peoples")
    ancient_name = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="Name commonly used by ancient peoples")
    coordinates = PointField()
    notes_easting_northing = models.TextField(
        help_text="The original coordinate system of record. "
                  "This value has been projected into lat/lon,"
                  " and should not be used directly.")
    area = models.FloatField(
        null=True, blank=True,
        help_text="Area in Hectares")
    survey_type = models.CharField(
        default="", choices=SURVEY_CHOICES)
    notes = models.TextField(default="")
    region = models.ForeignKey(Region, null=True, blank=True)
    references = models.ManyToManyField('bibliography.Publication')


class Feature(models.Model):
    """
    Important characteristics of an archaeological site

    Examples:
        - Tel
        - Fortification
        - EBIV
        -
    """
    shortname = models.CharField(max_length=10, unique=True)  # e.g. EBIV
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    sites = models.ManyToManyField(
        Site, related_name='tags', through='SiteFeatureTag'
    )


class SiteFeatureTag(models.Model):
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


class Period(RecursiveModel):
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



class Burial(Feature):
    """
    A Site might contain Burial structure, but it will only be tagged with
    one of these possible types
    """
    TOMB = 'tomb'
    CARIN = 'carin'
    CEMETARY = 'cemetary'

    BURIAL_TYPES = [
        (TOMB, 'Tomb'),
        (CARIN, 'Carins'),
        (CEMETARY, 'Cemetary'),
    ]
    burial_type = models.CharField(max_length=50, choices=BURIAL_TYPES)
