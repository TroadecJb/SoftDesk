from rest_framework import serializers
from account.models.CustomUser import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
