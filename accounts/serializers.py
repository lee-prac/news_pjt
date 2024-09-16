from rest_framework import serializers
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["user_id", "password", "nickname", "name", "email", "bio"]
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호는 읽기 전용
        }
