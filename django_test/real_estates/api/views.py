"""View set for the real estate app."""
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    mixins,
    permissions,
    viewsets,
)
from rest_framework.authentication import TokenAuthentication

from .serializers import PropertySerializer
from .permissions import IsOwnerOrSuperuser
from django_test.real_estates.models import Property


class PropertyViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """View set for the real estate property"""
    queryset = Property.objects.exclude(status='deleted')  # exclude status has been deleted
    serializer_class = PropertySerializer  # specific Serializer class
    authentication_classes = [TokenAuthentication]  # specific Authentication type
    pagination_class = PageNumberPagination  # Add this line to enable pagination

    # set filter by requirement
    filterset_fields = {
        'suburb': ['exact'],
        'for_sale_or_lease': ['exact'],
        'price': ['range'],
        'status': ['exact'],
        'created_at': ['exact', 'gte', 'lte'],
        'modified_at': ['exact', 'gte', 'lte'],
    }

    # set order by requirement
    ordering_fields = ['price', 'created_at', 'modified_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # For list and retrieve actions, allow any GET request without authentication.
            return [permissions.AllowAny()]
        else:
            # For create, update, partial_update, and destroy actions, restrict to owner or superuser.
            return [IsAuthenticated(), IsOwnerOrSuperuser()]
