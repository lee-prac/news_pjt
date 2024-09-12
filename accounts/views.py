from rest_framework import generics
from .serializers import SignupSerializer


# 회원가입 뷰
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
