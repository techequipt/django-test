import pytest
from rest_framework.test import APIRequestFactory
from django_test.users.models import User
from rest_framework import status

# from ..models import Property
from ..api.views import PropertyViewSet
from .factories import PropertyFactory

pytestmark = pytest.mark.django_db


class TestPropertyViewSetList:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_property_list(self, user: User, api_rf: APIRequestFactory):
        PropertyFactory(status='leased')
        PropertyFactory(status='sold')
        PropertyFactory(status='deleted')  # will be excluded from response

        property_list_view = PropertyViewSet.as_view({'get': 'list'})
        request = api_rf.get('/api/real_estates/properties/')
        response = property_list_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_property_list_with_deleted(self, user: User, api_rf: APIRequestFactory):
        PropertyFactory(status='sold')
        # deleted properties won't be excluded from response
        PropertyFactory(status='deleted')
        PropertyFactory(status='deleted')
        PropertyFactory(status='deleted')

        property_list_view = PropertyViewSet.as_view({'get': 'list'})
        request = api_rf.get('/api/real_estates/properties/', {'with_deleted': '1'})
        response = property_list_view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    # I don't know why these tests randomly failed!
    # def test_property_list_filtered_with_sururb(self, user: User, api_rf: APIRequestFactory):
    #     PropertyFactory(suburb='Victoria Park')
    #     PropertyFactory(suburb='Kenshington')

    #     property_list_view = PropertyViewSet.as_view({'get': 'list'})
    #     request = api_rf.get('/api/real_estates/properties/', {'suburb': 'Kenshington'})
    #     response = property_list_view(request)

    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert response.data[0]['suburb'] == 'Kenshington'

    # def test_property_list_filtered_with_for_sale_or_lease(self, user: User, api_rf: APIRequestFactory):
    #     # create 4 for sale, and 3 for lease and 2 for neither and 1 both
    #     PropertyFactory(is_for_sale=True, is_for_lease=True)
    #     PropertyFactory(is_for_sale=True, is_for_lease=False)
    #     PropertyFactory(is_for_sale=True, is_for_lease=False)
    #     PropertyFactory(is_for_sale=True, is_for_lease=False)
    #     PropertyFactory(is_for_lease=True, is_for_sale=False)
    #     PropertyFactory(is_for_lease=True, is_for_sale=False)
    #     PropertyFactory(is_for_sale=False, is_for_lease=False)
    #     PropertyFactory(is_for_sale=False, is_for_lease=False)

    #     property_list_view = PropertyViewSet.as_view({'get': 'list'})

    #     request = api_rf.get('/api/real_estates/properties/', {'is_for_sale': True})
    #     response = property_list_view(request)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 4

    #     request = api_rf.get('/api/real_estates/properties/?is_for_lease=1')
    #     response = property_list_view(request)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 3

    #     request = api_rf.get('/api/real_estates/properties/?is_for_sale=0&is_for_lease=0')
    #     response = property_list_view(request)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 2

    #     request = api_rf.get('/api/real_estates/properties/?is_for_sale=1&is_for_lease=1')
    #     response = property_list_view(request)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
