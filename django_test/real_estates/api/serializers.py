"""Serializers for real estate """
from rest_framework import serializers

from django_test.real_estates.models import Property


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property model"""
    class Meta:
        model = Property
        fields = [
            'id',
            'address',
            'suburb',
            'for_sale_or_lease',
            'price',
            'status',
            'created_at',
            'modified_at',
            'created_by',
            'modified_by']
        read_only_fields = ['id', 'created_at', 'created_by']
