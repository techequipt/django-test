from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Property
from .serializers import PropertySerializer


class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.exclude(status='deleted')
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['suburb', 'is_for_sale', 'is_for_lease', 'price', 'status']
    ordering_fields = ['price', 'created_at', 'updated_at']

    def get_permissions(self):
        if self.action == 'list':
            return []  # everyone can see list of properties
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Property.objects.all()
        with_deleted_param = self.request.query_params.get('with_deleted', '')
        with_deleted = False if with_deleted_param in ['0', 'false'] else with_deleted_param

        if not with_deleted:  # exclude deleted by default
            queryset = queryset.exclude(status='deleted')

        return queryset
