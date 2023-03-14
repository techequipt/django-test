from rest_framework import viewsets

from ..Permissions import IsAdminPermission, IsPropertyOwner
from ..models import Property
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from ..serializers.property_serializers import ProperySerializer


class PropertyFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['title', 'address', 'status', 'is_lease']


class PropertyViewset(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = ProperySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter

    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [IsPropertyOwner, IsAdminPermission]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
