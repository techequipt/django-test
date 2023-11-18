from django.test import RequestFactory, TestCase
from django_test.users.models import User
from django_test.properties.models import Property
from django_test.properties.permissions import IsAdminPermission, IsOwnerOrReadOnly

class PermissionTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create(username='admin', is_superuser=True)
        self.normal_user = User.objects.create(username='normaluser', is_superuser=False)
        self.factory = RequestFactory()

    def test_user_has_admin_permission(self):
        request = self.factory.delete('/')
        request.user = self.admin_user

        permission_check = IsAdminPermission()
        permission = permission_check.has_permission(request, None)

        self.assertTrue(permission)

    def test_user_has_not_admin_permission(self):
        request = self.factory.delete('/')
        request.user = self.normal_user

        permission_check = IsAdminPermission()
        permission = permission_check.has_permission(request, None)

        self.assertFalse(permission)

    def test_user_is_owner_property(self):
        request = self.factory.delete('/')
        request.user = self.normal_user
        mockProp = Property(id=1, created_by='normaluser')

        permission_check = IsOwnerOrReadOnly()
        permission = permission_check.has_object_permission(request, None, mockProp)

        self.assertTrue(permission)

    def test_user_is_not_owner_property(self):
        request = self.factory.delete('/')
        request.user = self.normal_user
        mockProp = Property(id=2, created_by='admin')

        permission_check = IsOwnerOrReadOnly()
        permission = permission_check.has_object_permission(request, None, mockProp)

        self.assertFalse(permission)
