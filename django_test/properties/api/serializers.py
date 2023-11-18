from rest_framework import serializers
from django_test.properties.models import Property

class ProperySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'