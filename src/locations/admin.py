from django.contrib import admin
from .models import Site, Region, Period, SiteFeature, Feature


class SiteFeatureInline(admin.TabularInline):
    model = SiteFeature


class SiteAdmin(admin.ModelAdmin):
    list_display = ('code', 'modern_name', 'region')
    inlines = [
        SiteFeatureInline,
    ]


class RegionAdmin(admin.ModelAdmin):
    """
    View/edit which sites are in a given region.
    """
    list_display = ('name', 'description')


class FeatureAdmin(admin.ModelAdmin):
    """
    Features such as "Tel" or "Fortress" or "Walls"
    """


class PeriodAdmin(admin.ModelAdmin):
    """
    Admin to display period information
    """
    list_display = ('shortname', 'start', 'end',  'name', 'description', )
    list_editable = ('start', 'end')


admin.site.register(Region, RegionAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Feature, FeatureAdmin)

# Register your models here.
