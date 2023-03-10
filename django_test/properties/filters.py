from django_filters import rest_framework as filters

from .models import Property


class PropertyOrderingFilter(filters.OrderingFilter):
    def __init__(self):
        super().__init__(
            fields={
                "price": "price",
                "created_at": "created_at",
                "updated_at": "updated_at",
            }
        )

class PropertyFilter(filters.FilterSet):
    address = filters.CharFilter(lookup_expr='iexact')
    type = filters.NumberFilter()
    status = filters.NumberFilter()
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    order_by = PropertyOrderingFilter()

    class Meta:
        model = Property
        fields = ["address", "type", "status", "price"]
