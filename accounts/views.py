from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .validators import validate_user_data, validate_password_change
from .serializers import SignupSerializer

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
            bio=request.data.get("bio")
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
            return Response({"message": "아이디, 패스워드가 일치하지 않거나, 없는 계정입니다."}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"message": "리프레시 토큰이 필요합니다."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            # 토큰을 블랙리스트에 추가
            token.blacklist()
        except Exception as e:
            return Response({"message": "토큰 처리 중 오류가 발생했습니다."}, status=400)

        response = Response({"message": "로그아웃 되었습니다."}, status=200)
        response.delete_cookie("refreshtoken")
        return response


# 회원탈퇴
class WithdrawView(APIView):
    def delete(self, request):
        password = request.data.get("password")
        if not request.user.check_password(password):
            return Response({"message": "비밀번호를 다시 입력해주세요."}, status=400)

        request.user.is_active = False
        request.user.save()
        return Response({"message": "계정이 성공적으로 탈퇴되었습니다."}, status=204)


# 비밀번호 변경
class PasswordChangeView(APIView):
    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        rlt_message = validate_password_change(
            new_password, old_password, request.user)
        if rlt_message:
            return Response({"message": rlt_message}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 변경 처리
        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)