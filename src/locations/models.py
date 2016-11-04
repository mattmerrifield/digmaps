from django.db import models

class SiteType(models.Model):
    """
    Different Types of archeological site
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)


class BurialType(models.Model):
    """
    Different types of burials
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)


class SiteFunction(models.Model):
    """
    Different uses for a given site
    """

    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)


class Citation(models.Model):
    """
    An academic citation (short form)
    """
    author = models.CharField(max_length=50)
    publication = models.TextField()

    def __str__(self):
        return "{}".format(self.author)


class Geology(models.Model):
    """
    A classification of geological features, e.g. how hard are the rocks? How
    sandy is region? Rainfall? You know. Geology and shit.
    """
    class Meta:
        verbose_name_plural = "geologies"

    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)


class Region(models.Model):
    """
    A general area.
    """
    parent = models.ForeignKey("self", null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{}".format(self.name)


class Period(models.Model):
    """
    An archeological period, e.g. "Early Bronze Age"
    """
    shortname = models.CharField(max_length=50, unique=True)  # e.g. EBIV
    name = models.CharField(max_length=50)       # e.g. Early Bronze IV
    description = models.TextField()

    def __str__(self):
        return self.shortname


class Site(models.Model):
    """
    An archaeological site.
    """
    site_id = models.IntegerField()  # ID the site survey uses
    modern_name = models.CharField(max_length=50, null=True, blank=True)
    ancient_name = models.CharField(max_length=50, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    site_size = models.FloatField(help_text="Area in Hectares", null=True, blank=True)

    # Basic Descriptors
    region = models.ForeignKey(Region, null=True, blank=True)
    geology = models.ManyToManyField(Geology, null=True, blank=True)
    site_type = models.ForeignKey(SiteType, null=True, blank=True)
    burial_type = models.ManyToManyField(BurialType, null=True, blank=True)
    site_function = models.ManyToManyField(SiteFunction, null=True, blank=True)
    reference = models.ManyToManyField(Citation, null=True, blank=True)
    period = models.ManyToManyField(Period, null=True, blank=True)

    notes = models.TextField(default="")


