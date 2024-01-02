from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_test.real_estates.api.views import PropertyViewSet
from django_test.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("real_estates/properties", PropertyViewSet)


app_name = "api"
urlpatterns = router.urls
