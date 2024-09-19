from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
import string


def validate_user_data(user_data):
    email = user_data.get("email")
    nickname = user_data.get("nickname")
    bio = user_data.get("bio")

    # email
    if not email:
        return "이메일을 입력해주세요."

    if CustomUser.objects.filter(email=email).exists():
        return "이미 존재하는 이메일입니다."

    try:
        validate_email(email)
    except ValidationError:
        return "유효하지 않은 이메일 형식입니다."

    # nickname
    if not nickname:
        return "닉네임을 입력해주세요."

    if CustomUser.objects.filter(nickname=nickname).exists():
        return "이미 존재하는 닉네임입니다."

    if not (2 <= len(nickname) <= 20) or " " in nickname or not nickname.isalnum():
        return "닉네임은 2자 이상, 20자 이하로 입력해야 하며, 공백 또는 특수문자를 포함할 수 없습니다."

    # bio
    if len(bio) > 300:
        return "자기소개는 300자 까지 입력 가능합니다."
