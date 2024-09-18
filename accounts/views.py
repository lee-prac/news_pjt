from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, LoginSerializer, LogoutSerializer
from rest_framework.views import APIView
# Create your views here.


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteAPIView(APIView):
    def delete(self, request):
        password = request.data.get("password")
        if not request.user.check_password(password):
            return Response({"message": "비밀번호를 다시 입력해주세요."}, status=400)

        request.user.is_active = False
        request.user.save()
        return Response({"message": "계정이 성공적으로 탈퇴되었습니다."}, status=204)