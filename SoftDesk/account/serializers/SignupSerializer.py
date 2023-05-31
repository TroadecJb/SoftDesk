from rest_framework import serializers
from account.models.CustomUser import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    """Signup serializer."""

    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = CustomUser.objects.create(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords don't match."}
            )
        user.set_password(self.validated_data["password"])
        user.save()
        return user
