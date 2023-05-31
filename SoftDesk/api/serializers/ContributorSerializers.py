from rest_framework import serializers
from api.models.Contributor import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """Contributor serializer."""

    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "permission",
            "role",
        ]
