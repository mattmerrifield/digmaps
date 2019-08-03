"""digmaps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from locations.views import router as location_router
from django.conf.urls import url
from graphene_django.views import GraphQLView

urlpatterns = [
    # Everything in this website needs to be behind the api/ path, or nginx will not
    # direct the traffic here
    url(r"^api/admin/", admin.site.urls),
    url(r"^api/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r"^api/rfxml", include(location_router.urls)),
]
