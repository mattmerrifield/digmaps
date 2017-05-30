from django.db import models
from django.contrib.gis.db.models import PointField


class Citation(models.Model):
    """
    An academic citation (short form)
    """
    site = models.ForeignKey('Site')
    publication = models.ForeignKey('bibliography.Publication')
    external_id = models.CharField(
        max_length=100,
        help_text="The ID number assigned to the site by the publication "
                  "authors (e.g. 'ASI85-35' or 'BSL-123'"
    )

    def __str__(self):
        return "{}".format(self.publication)


class Region(models.Model):
    """
    A general geographical area.

    Can be nested. Be cautious when making queries for sites in a given region
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, related_name='children')

    def parent_regions(self, include_self=True, depth=None):
        """
        Returns a list of Regions for whom self is a sub-region
        """
        ancestors = [self] if include_self else []
        parent = self.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

    def child_regions(self, include_self=True):
        family = []
        for r in self.children.all():
            family.extend(r.child_regions())
        if include_self:
            family.append(
                self)  # Parent goes last, to follow recursion pattern
        return family

    def __str__(self):
        return "{} {}".format(self.id, self.name)


class Site(models.Model):
    """
    An archaeological site.
    """
    modern_name = models.CharField(max_length=50, null=True, blank=True)
    ancient_name = models.CharField(max_length=50, null=True, blank=True)
    coordinates = PointField()
    area = models.FloatField(null=True, blank=True, help_text="Area in Hectares",)
    references = models.ManyToManyField('bibliography.Publication', through=Citation)
    notes = models.TextField(default="")
    region = models.ForeignKey(Region, null=True, blank=True)


class SiteTag(models.Model):
    """
    Standard Through-model for tagging a site, but allows the "maybe" flag to
    be set for the relationship
    """
    site = models.ForeignKey('Site')
    tag = models.ForeignKey('Tag')
    uncertain = models.BooleanField(default=False,
                                    help_text="Evidence for for this tag on "
                                              "this site is not conclusive")

    class Meta:
        unique_together = ('site', 'tag')


class Tag(models.Model):
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
    sites = models.ManyToManyField(Site, related_name='tags',
                                   through='SiteTag')


class Period(Tag):
    """
    An archaeological period, e.g. "Early Bronze Age"

    Semantically, a SiteTag with extra metadata
    """
    start = models.IntegerField(help_text="Approximate Beginning (BCE is negative)")
    end = models.IntegerField(help_text="Approximate Ending (BCE is negative)")

    def __str__(self):
        return self.shortname


class Burial(Tag):
    """
    A Site might contain Burial structure, but it will only be tagged with
    one of these possible types
    """
    BURIAL_TYPES = [
        ('tomb', 'Tomb'),
        ('carins', 'Carins'),
        ('cemetary', 'Cemetary'),
    ]
    type = models.CharField(max_length=50, choices=BURIAL_TYPES)
