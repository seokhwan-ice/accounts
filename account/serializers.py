from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "name",
            "profile_image",
            "phone_number",
            "bio",
        ]