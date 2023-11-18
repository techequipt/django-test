from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from .api import (views)

router = routers.DefaultRouter()
router.register('properties', views.PropertyViewset)

urlpatterns = [
    path('', include(router.urls)),
]