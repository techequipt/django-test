from rest_framework import viewsets
from ..models import Property
from ..permissions import IsAdminPermission, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from .serializers import ProperySerializer
from ..constants import (DELETED)

class PropertyFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['address', 'is_suburb', 'is_sale', 'status']

class PropertyViewset(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = ProperySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PropertyFilter
    ordering_fields = ['price', 'created_at', 'last_modified']
    ordering = ['price', 'created_at', 'last_modified']

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'destroy': 
            permission_classes = [IsAuthenticated, IsAdminPermission | IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status == DELETED: 
            return super().get_queryset().filter(status=DELETED)
        else:
            return super().get_queryset().exclude(status=DELETED)
            