import pytest
from rest_framework.test import APIRequestFactory
from django_test.users.models import User
from rest_framework import status

from django_test.users.tests.factories import UserFactory
from ..api.views import PropertyViewSet
from .factories import PropertyFactory

pytestmark = pytest.mark.django_db


class TestPropertyViewSetUpdatePermissions:
    @pytest.fixture
    def api_rf(self): return APIRequestFactory()

    def test_property_updating_unauthenticated(self, user: User, api_rf: APIRequestFactory):
        property = PropertyFactory(status='available')
        request = api_rf.patch(f'/api/real_estates/properties/{property.id}', {'status': 'sold'})

        property_list_view = PropertyViewSet.as_view({'patch': 'partial_update'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_property_updating_not_by_owner(self, user: User, api_rf: APIRequestFactory):
        property_owner = UserFactory()
        property = PropertyFactory(status='available', created_by=property_owner)

        request = api_rf.patch(f'/api/real_estates/properties/{property.id}', {'status': 'sold'})
        request.user = user  # request.user is not property_owner

        property_list_view = PropertyViewSet.as_view({'patch': 'partial_update'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_property_updating_by_owner(self, user: User, api_rf: APIRequestFactory):
        property = PropertyFactory(status='available', created_by=user)

        request = api_rf.patch(f'/api/real_estates/properties/{property.id}', {'status': 'sold'})
        request.user = user  # request.user is property_owner

        property_list_view = PropertyViewSet.as_view({'patch': 'partial_update'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_200_OK

    def test_property_updating_by_superuser(self, user: User, api_rf: APIRequestFactory):
        property = PropertyFactory(status='available', created_by=user)

        superuser = UserFactory(is_superuser=True)
        request = api_rf.patch(f'/api/real_estates/properties/{property.id}', {'status': 'sold'})
        request.user = superuser  # request.user is not property_owner but a superuser

        property_list_view = PropertyViewSet.as_view({'patch': 'partial_update'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_200_OK


class TestPropertyViewSetDeletePermissions:
    @pytest.fixture
    def api_rf(self): return APIRequestFactory()

    def test_property_deleting_unauthenticated(self, user: User, api_rf: APIRequestFactory):
        property = PropertyFactory(status='available')
        request = api_rf.delete(f'/api/real_estates/properties/{property.id}')

        property_list_view = PropertyViewSet.as_view({'delete': 'destroy'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_property_deleting_not_by_owner(self, user: User, api_rf: APIRequestFactory):
        property_owner = UserFactory()
        property = PropertyFactory(status='available', created_by=property_owner)

        request = api_rf.delete(f'/api/real_estates/properties/{property.id}')
        request.user = user  # request.user is not property_owner

        property_list_view = PropertyViewSet.as_view({'delete': 'destroy'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_property_deleting_by_owner(self, user: User, api_rf: APIRequestFactory):
        property = PropertyFactory(status='available', created_by=user)

        request = api_rf.delete(f'/api/real_estates/properties/{property.id}')
        request.user = user  # request.user is property_owner

        property_list_view = PropertyViewSet.as_view({'delete': 'destroy'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_property_deleting_by_superuser(self, user: User, api_rf: APIRequestFactory):
        property = PropertyFactory(status='available', created_by=user)

        superuser = UserFactory(is_superuser=True)
        request = api_rf.delete(f'/api/real_estates/properties/{property.id}')
        request.user = superuser  # request.user is not property_owner but a superuser

        property_list_view = PropertyViewSet.as_view({'delete': 'destroy'})
        response = property_list_view(request, id=property.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
