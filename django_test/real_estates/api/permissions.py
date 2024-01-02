"""Permissions for supper user"""
from rest_framework import permissions


class IsOwnerOrSuperuser(permissions.BasePermission):
    """Custom permission for only owners or supper user"""
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_superuser
