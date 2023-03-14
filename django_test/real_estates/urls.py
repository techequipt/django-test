from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .api import (property_view)

router = routers.DefaultRouter()
router.register('properties', property_view.PropertyViewset)

urlpatterns = [
    path('', include(router.urls)),
]
