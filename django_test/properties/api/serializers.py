from rest_framework import serializers

from ..models import Property


class PropertySerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = request.user
        validated_data['created_by'] = user
        return super().create(validated_data)

    class Meta:
        model = Property
        fields = ["address", "type", "status", "price", "created_at", "updated_at"]

        extra_kwargs = {
            "read_only": {"created_at": "updated_at",}
        }
