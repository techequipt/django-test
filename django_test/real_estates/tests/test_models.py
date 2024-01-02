"""
Test the models real estate
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from django_test.real_estates.models import Property


def create_user(username='test1', password='pass@123'):
    """Create a new user"""
    return get_user_model().objects.create_user(username=username, password=password)


class ModelTests(TestCase):
    """Test model"""

    def setUp(self):
        """Test create and setup"""
        self.user_test = create_user()

    def test_property_creation(self):
        # data for test creation
        property_data = {
            'address': "123 test address st",
            'suburb': "test Suburb",
            'for_sale_or_lease': True,
            'price': Decimal('30.02'),
            'status': "available",
            'created_by': self.user_test,
        }

        # Create a property instance
        property_instance = Property.objects.create(
            **property_data
        )

        # Query the database to retrieve the created property
        retrieved_property = Property.objects.get(id=property_instance.id)

        # Check if the property was created with the expected values
        self.assertEqual(retrieved_property.address, property_data['address'])
        self.assertEqual(retrieved_property.suburb, property_data['suburb'])
        self.assertEqual(retrieved_property.for_sale_or_lease, property_data['for_sale_or_lease'])
        self.assertEqual(retrieved_property.price, property_data['price'])
        self.assertEqual(retrieved_property.status, property_data['status'])
        self.assertEqual(retrieved_property.created_by, property_data['created_by'])
        self.assertIsNotNone(retrieved_property.created_at)
        self.assertIsNotNone(retrieved_property.modified_at)
        self.assertIsNone(retrieved_property.modified_by)

    def test_property_str_method(self):
        STATUS_CHOICES = [
            ('available', 'Available'),
            ('sold', 'Sold'),
            ('leased', 'Leased'),
            ('deleted', 'Deleted'),
        ]
        # data for test creation
        property_data = {
            'address': "123 test address st",
            'suburb': "test Suburb",
            'for_sale_or_lease': True,
            'price': Decimal('30.02'),
            'status': "available",
            'created_by': self.user_test,
        }

        # Create a property instance
        property_instance = Property.objects.create(
            **property_data
        )

        # Check if the __str__ method returns the expected string representation
        expected_str = (
            property_data['address'] + " - " +
            property_data['suburb'] + " - " +
            dict(STATUS_CHOICES)[property_data['status']]
        )
        self.assertEqual(str(property_instance), expected_str)
