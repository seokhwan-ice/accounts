from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "nickname",
            "name",
            "profile_image",
            "phone_number",
            "bio",
            
        ]


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="id")
    password = serializers.CharField(help_text="password")
    