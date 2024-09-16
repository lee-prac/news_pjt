from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .validators import validate_user_data
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny


# 회원가입
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        rlt_message = validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status=400)

        user = CustomUser.objects.create_user(
            user_id=request.data.get("user_id"),
            password=request.data.get("password"),
            name=request.data.get("name"),
            nickname=request.data.get("nickname"),
            email=request.data.get("email"),
            bio=request.data.get("bio"),
        )

        refresh = RefreshToken.for_user(user)

        serializer = SignupSerializer(user)
        response_dict = serializer.data
        response_dict["access"] = str(refresh.access_token)
        response_dict["refresh"] = str(refresh)
        return Response(response_dict)


# 로그인
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        user = authenticate(user_id=user_id, password=password)
        if not user:
            return Response(
                {"message": "아이디, 패스워드가 일치하지 않거나, 없는 계정입니다."},
                status=400,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
