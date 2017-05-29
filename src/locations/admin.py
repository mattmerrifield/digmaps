from django.contrib import admin
from .models import Site, Region, Period, Citation


class SiteAdmin(admin.ModelAdmin):
    pass


class NameDescriptionAdmin(admin.ModelAdmin):
    """
    An admin for name/description-style stuff
    """
    list_display = ('name', 'description')


class SiteInline(admin.TabularInline):
    model = Site


class RegionAdmin(NameDescriptionAdmin):
    """
    Admin allowing sites to be populated in a region
    """
    inlines = [
        SiteInline
    ]


class PeriodAdmin(NameDescriptionAdmin):
    """
    Admin to display period information
    """
    list_display = ('shortname', 'name', 'description')

admin.site.register(Site)
admin.site.register(Region, RegionAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Citation)

# Register your models here.
