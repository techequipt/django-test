from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from django_test.real_estates.models import Property


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_superuser is True


class IsPropertyOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        kwargs = view.kwargs
        property_id = kwargs.get('property_id', kwargs.get('pk', None))

        return Property.objects.filter(pk=property_id, created_by=request.user).exists()
