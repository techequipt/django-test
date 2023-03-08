import pytest
from rest_framework.test import APIRequestFactory

from django_test.properties.api.views import PropertyViewSet
from django_test.properties.models import Property

# TODO: Cannnot do this part.
class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()
