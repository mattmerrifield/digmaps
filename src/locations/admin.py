from django.contrib import admin
from .models import Site, Region, Period, Citation, Tag


class CitationInline(admin.TabularInline):
    model = Citation


class SiteAdmin(admin.ModelAdmin):
    inlines = [
        CitationInline
    ]


class TagAdmin(admin.ModelAdmin):
    """
    An admin for name/description-style stuff
    """
    list_display = ('shortname', 'name', 'description')


class RegionAdmin(admin.ModelAdmin):
    """
    Admin allowing sites to be populated in a region
    """


class PeriodAdmin(TagAdmin):
    """
    Admin to display period information
    """
    list_display = TagAdmin.list_display + ('start', 'end')
    list_editable = ('start', 'end')

admin.site.register(Site, SiteAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Period, PeriodAdmin)

# Register your models here.
