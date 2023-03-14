from rest_framework import serializers
from django_test.real_estates.models import Property


class ProperySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'is_deleted': {'read_only': True},
        }
