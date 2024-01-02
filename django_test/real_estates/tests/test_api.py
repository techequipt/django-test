# tests.py
from decimal import Decimal

from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model

from django_test.real_estates.models import Property
from django_test.real_estates.api.serializers import PropertySerializer

REAL_ESTATES_PROPERTY_URL = '/api/real_estates/properties/'


def detail_url(property_id):
    """Create and return the detail URL"""
    return f'/api/real_estates/properties/{property_id}/'


def create_user(username='test1', password='pass@123'):
    """Create a new user"""
    return get_user_model().objects.create_user(username=username, password=password)


def create_super_user(username='test_supper', password='pass@123'):
    """Create a new supper user"""
    return get_user_model().objects.create_superuser(username=username, password=password)


class PublicPropertyAPITest(TestCase):
    """Test the public api required for authenticated users"""

    def setUp(self):
        """Set up test"""
        self.current_user = create_user()
        self.other_user = create_user("test2", "pass@123")
        self.property11 = Property.objects.create(
            address="123 Test address St",
            suburb="Test1 Suburb",
            for_sale_or_lease=True,
            price=Decimal(3000.02),
            status="available",
            created_by=self.current_user
        )

        self.property12 = Property.objects.create(
            address="123 Test address St",
            suburb="Test1 Suburb",
            for_sale_or_lease=True,
            price=Decimal(10000.02),
            status="available",
            created_by=self.current_user
        )

        self.property2 = Property.objects.create(
            address="456 Test address St",
            suburb="Test2 Suburb",
            for_sale_or_lease=False,
            price=Decimal(7000.02),
            status="sold",
            created_by=self.current_user
        )

        self.property3 = Property.objects.create(
            address="789 Test address St",
            suburb="Test3 Suburb",
            for_sale_or_lease=True,
            price=Decimal(9000.02),
            status="leased",
            created_by=self.other_user
        )

        self.property4 = Property.objects.create(
            address="101112 Test address St",
            suburb="Test4 Suburb",
            for_sale_or_lease=False,
            price=Decimal(12000.02),
            status="deleted",
            created_by=self.current_user
        )

        self.client = APIClient()

    def test_retrieve_single_property_combined_filter(self):
        """Test retrieving a single property"""
        filter_for_sale_or_lease = True
        filter_suburb = 'Test1 Suburb'
        filter_status = 'available'

        filter_price_min = 3000
        filter_price_max = 4001

        created_at__gte = '2024-01-01 08:47:11.115476+00'
        created_at__lte = '2024-01-05 08:47:11.115476+00'

        modified_at__gte = '2024-01-01 08:47:11.115476+00'
        modified_at__lte = '2024-01-05 08:47:11.115476+00'

        response = self.client.get(
            REAL_ESTATES_PROPERTY_URL,
            data={
                'for_sale_or_lease': filter_for_sale_or_lease,
                'suburb': filter_suburb,
                'status': filter_status,
                'price__range': str(filter_price_min) + ',' + str(filter_price_max),
                'created_at__gte': created_at__gte, 'created_at__lte': created_at__lte,
                'modified_at__gte': modified_at__gte, 'modified_at__lte': modified_at__lte,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        properties = Property.objects.filter(
            for_sale_or_lease=filter_for_sale_or_lease,
            suburb=filter_suburb,
            created_by=self.current_user,
            price__range=(filter_price_min, filter_price_max),
            created_at__gte=created_at__gte,
            created_at__lte=created_at__lte,
            modified_at__gte=modified_at__gte,
            modified_at__lte=modified_at__lte,
        ).order_by('-price', '-created_at', '-modified_at')
        serializer = PropertySerializer(properties, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_retrieve_list_properties_combined_filter(self):
        """Test retrieving list properties"""
        filter_for_sale_or_lease = True
        filter_suburb = 'Test1 Suburb'
        filter_status = 'available'

        filter_price_min = 3000
        filter_price_max = 12001

        created_at__gte = '2024-01-01 08:47:11.115476+00'
        created_at__lte = '2024-01-05 08:47:11.115476+00'

        modified_at__gte = '2024-01-01 08:47:11.115476+00'
        modified_at__lte = '2024-01-05 08:47:11.115476+00'

        response = self.client.get(
            REAL_ESTATES_PROPERTY_URL,
            {
                'for_sale_or_lease': filter_for_sale_or_lease,
                'suburb': filter_suburb,
                'status': filter_status,
                'price__range': str(filter_price_min) + ',' + str(filter_price_max),
                'created_at__gte': created_at__gte, 'created_at__lte': created_at__lte,
                'modified_at__gte': modified_at__gte, 'modified_at__lte': modified_at__lte,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        properties = Property.objects.filter(
            for_sale_or_lease=filter_for_sale_or_lease,
            suburb=filter_suburb,
            created_by=self.current_user,
            price__range=(filter_price_min, filter_price_max),
            created_at__gte=created_at__gte,
            created_at__lte=created_at__lte,
            modified_at__gte=modified_at__gte,
            modified_at__lte=modified_at__lte,
        ).order_by('price', 'created_at', 'modified_at')
        serializer = PropertySerializer(properties, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_retrieve_excluded_deleted_status_property(self):
        response = self.client.get(
            REAL_ESTATES_PROPERTY_URL,
            {
                'suburb': 'Test4 Suburb'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_property_unauthenticated(self):
        payload = {
            "address": "string",
            "suburb": "string",
            "for_sale_or_lease": True,
            "price": "-4.03",
            "status": "available"
        }
        response = self.client.post(REAL_ESTATES_PROPERTY_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_property_unauthenticated(self):
        payload = {
            "address": "string",
            "suburb": "string",
            "for_sale_or_lease": True,
            "price": "-4.03",
            "status": "available"
        }

        url = detail_url('1')
        print(url)
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_property_unauthenticated(self):
        payload = {
            "address": "string",
            "suburb": "string",
            "for_sale_or_lease": True,
            "price": "-4.03",
            "status": "available"
        }

        url = detail_url('1')
        print(url)
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_property_unauthenticated(self):
        payload = {
            "address": "string",
            "suburb": "string",
            "for_sale_or_lease": True,
            "price": "-4.03",
            "status": "available"
        }

        url = detail_url('1')
        print(url)
        response = self.client.delete(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNormalUserPropertyAPITest(TestCase):
    """ Test normal user"""

    def setUp(self):
        self.current_user = create_user()
        self.other_user = create_user("test2", "pass@123")
        self.property11 = Property.objects.create(
            address="123 Test address St",
            suburb="Test1 Suburb",
            for_sale_or_lease=True,
            price=Decimal(3000.02),
            status="available",
            created_by=self.other_user
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.current_user)

    def test_create_property_success(self):
        payload = {
            "address": "test address St",
            "suburb": "test suburb",
            "for_sale_or_lease": True,
            "price": Decimal(10.00),
            "status": "available"
        }
        response = self.client.post(REAL_ESTATES_PROPERTY_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        property_db = Property.objects.get(id=response.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(property_db, k), v)

        self.assertEqual(property_db.created_by, self.current_user)

    def test_full_update_property_success(self):

        property_origin = Property.objects.create(
            address="123 Test address St",
            suburb="Test1 Suburb",
            for_sale_or_lease=True,
            price=Decimal('3000.02'),
            status="available",
            created_by=self.current_user
        )

        payload = {
            "address": "123 Test address St updated",
            "suburb": "Test1 Suburb updated",
            "for_sale_or_lease": False,
            'price': Decimal('5000.02'),
            "status": "sold"
        }

        url = detail_url(property_origin.id)
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        property_origin.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(property_origin, k), v)

        self.assertEqual(property_origin.created_by, self.current_user)

    def test_delete_property_success(self):

        property_delete = Property.objects.create(
            address="123 Test address St",
            suburb="Test1 Suburb",
            for_sale_or_lease=True,
            price=Decimal('3000.02'),
            status="available",
            created_by=self.current_user
        )

        url = detail_url(property_delete.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Property.objects.filter(id=property_delete.id).exists())

    def test_full_update_property_forbidden(self):

        payload = {
            "address": "123 Test address St updated",
            "suburb": "Test1 Suburb updated",
            "for_sale_or_lease": False,
            'price': Decimal('5000.02'),
            "status": "sold"
        }

        url = detail_url(self.property11.id)
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.property11.refresh_from_db()
        for k, v in payload.items():
            self.assertNotEqual(getattr(self.property11, k), v)

        self.assertNotEqual(self.property11.created_by, self.current_user)

    def test_delete_property_forbidden(self):

        url = detail_url(self.property11.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.property11.refresh_from_db()
        self.assertTrue(Property.objects.filter(id=self.property11.id).exists())


class PrivateSupperUserPropertyAPITest(TestCase):
    """ Test supper user"""

    def setUp(self):
        self.current_user = create_super_user()
        self.other_user = create_user("test2", "pass@123")
        self.property11 = Property.objects.create(
            address="123 Test address St",
            suburb="Test1 Suburb",
            for_sale_or_lease=True,
            price=Decimal(3000.02),
            status="available",
            created_by=self.other_user
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.current_user)

    def test_full_update_property_other_owner_success(self):
        payload = {
            "address": "123 Test address St updated",
            "suburb": "Test1 Suburb updated",
            "for_sale_or_lease": False,
            'price': Decimal('5000.02'),
            "status": "sold"
        }

        url = detail_url(self.property11.id)
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.property11.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(self.property11, k), v)

    def test_delete_property_other_owner_success(self):
        url = detail_url(self.property11.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Property.objects.filter(id=self.property11.id).exists())
