from rest_framework import serializers
from .models import CustomUser


# 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "name", "password", "nickname", "bio", "email"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])  # 비밀번호 해시화
        user.save()
        return user
