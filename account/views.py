from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .validators import validate_user_data
from .serializers import (
    UserSerializer,
    )


class UserCreateView(APIView):
    def post(self, request):
        # 유효성 검사
        rlt_message = validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status=400)

        validated_data = {
            "username": request.data.get("username"),
            "nickname": request.data.get("nickname"),
            "name": request.data.get("name"),
            "password": request.data.get("password"),
            "bio": request.data.get("bio"),
            "profile_image": request.data.get("profile_image"),
            "phone_number": request.data.get("phone_number"),
            "email": request.data.get("email"),
        }

        user = User.objects.create_user(**validated_data)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)