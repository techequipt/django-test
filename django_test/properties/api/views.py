from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import PropertySerializer
from ..models import Property
from ..choices import PropertyStatus
from ..filters import PropertyFilter
from ...users.permissions import IsSuperUser


class PropertyViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    lookup_field = "id"
    filterset_class = PropertyFilter
    
    def check_object_permissions(self, request, obj):
        if obj.created_by != request.user or not request.user.is_superuser:
            raise PermissionDenied(
                detail='You do not have permission')
        return super().check_object_permissions(request, obj)

    def get_queryset(self, *args, **kwargs):
        return self.queryset.exclude(status=PropertyStatus.DELETED)
    
    def perform_update(self, serializer):
        self.check_object_permissions(self.request, self.get_object())
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.status = PropertyStatus.DELETED
        instance.save()

