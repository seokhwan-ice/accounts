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
    UserSignupSerializer
    )
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserCreateView(APIView):
    
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: openapi.Response('Signup successful', UserSerializer)}
    )    
    
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
    


class UserSigninView(APIView):
    @swagger_auto_schema(
    request_body=UserSignupSerializer,
    responses={201: openapi.Response('Login successful', UserSignupSerializer)}
)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"message": "아이디 또는 비밀번호가 틀렸습니다"}, status=400
            )

        refresh = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_info": serializer.data,
            }
        )