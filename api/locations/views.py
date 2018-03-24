from rest_framework import viewsets, routers


from locations import serializers, models


class LocationModelViewSet(viewsets.ModelViewSet):

    permission_classes = []


# The viewsets are bog-standard
class SiteViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH).
    """
    queryset = models.Site.objects.all()
    serializer_class = serializers.SiteSerializer


class FeatureViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH).
    """
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer


class PeriodViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH).
    """
    queryset = models.Period.objects.all()
    serializer_class = serializers.PeriodSerializer


class RegionViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH)
    """
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer


# The four main resources are available at top-level simple URLs, for GET/POST/PATCH/PUT/DELETE etc.
router = routers.DefaultRouter(trailing_slash=True)
router.register(r'sites', SiteViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'regions', RegionViewSet)

