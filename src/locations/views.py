from rest_framework import viewsets
from rest_framework_extensions import routers
from rest_framework_extensions.mixins import NestedViewSetMixin


from locations import serializers


class LocationModelViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = []


# The viewsets are bog-standard
class SiteViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH).
    """
    serializer_class = serializers.SiteSerializer


class FeatureViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH).
    """
    serializer_class = serializers.FeatureSerializer


class PeriodViewSet(LocationModelViewSet):
    """
    Supports standard actions: Retrieve, List, Create, Update (PUT), Partial Update (PATCH).
    """
    serializer_class = serializers.PeriodSerializer


# The three main resources are available at top-level simple URLs, for GET/POST/PATCH/PUT/DELETE etc.
router = routers.ExtendedSimpleRouter()
(
    router.register(r'sites', SiteViewSet)
          .register(r'feature', FeatureViewSet, parents_query_lookups=['site__features'])
          .register(r'periods', PeriodViewSet, parents_query_lookups=['site__periods'])
)
urlpatterns = router.urls

# One-level of nesting is provided by a fancy custom router
