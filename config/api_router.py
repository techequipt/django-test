from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_test.users.api.views import UserViewSet
from django_test.properties.api.views import PropertyViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("properties", PropertyViewSet)


app_name = "api"
urlpatterns = router.urls
