from django.test import TestCase
from django_test.users.models import User

from ..models import Property

class PropertyModelTest(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_real_estate_property_creation(self):
        # Test that a Property instance can be created
        property = Property.objects.create(
            address='123 Main St',
            suburb='Sample Suburb',
            is_for_sale=True,
            is_for_lease=False,
            status='available',
            price=100000.00,
            created_by=self.user
        )

        self.assertEqual(property.address, '123 Main St')
        self.assertEqual(property.suburb, 'Sample Suburb')
        self.assertTrue(property.is_for_sale)
        self.assertFalse(property.is_for_lease)
        self.assertEqual(property.status, 'available')
        self.assertEqual(property.price, 100000.00)
        self.assertEqual(property.created_by, self.user)

    def test_real_estate_property_str_method(self):
        # Test the __str__ method of the Property model
        property = Property.objects.create(
            address='456 Oak St',
            suburb='Another Suburb',
            is_for_sale=False,
            is_for_lease=True,
            status='leased',
            price=75000.50,
            created_by=self.user
        )

        self.assertEqual(str(property), '456 Oak St - Leased')

    def test_real_estate_property_default_values(self):
        # Test that default values are correctly set
        property = Property.objects.create(address='789 Elm St', created_by=self.user)

        self.assertFalse(property.is_for_sale)
        self.assertFalse(property.is_for_lease)
        self.assertEqual(property.status, 'available')
        self.assertIsNone(property.price)

    def test_real_estate_property_auto_timestamps(self):
        # Test that the timestamps are automatically set
        property = Property.objects.create(address='987 Pine St', created_by=self.user)

        self.assertIsNotNone(property.created_at)
        self.assertIsNotNone(property.updated_at)

        initial_created_at = property.created_at
        property.save()

        self.assertEqual(property.created_at, initial_created_at)
        self.assertNotEqual(property.updated_at, initial_created_at)
