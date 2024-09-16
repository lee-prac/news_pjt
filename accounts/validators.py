from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser
import string


def validate_user_data(user_data):
    user_id = user_data.get("user_id")
    email = user_data.get("email")
    nickname = user_data.get("nickname")
    password = user_data.get("password")
    bio = user_data.get("bio")

    # user_id
    if not user_id:
        return "아이디를 입력해주세요."

    if CustomUser.objects.filter(user_id=user_id).exists():
        return "이미 존재하는 아이디입니다."

    if len(user_id) < 4 or " " in user_id or not user_id.isalnum(): 
        return "아이디는 최소 4자 이상이어야 하며, 공백 또는 특수문자를 포함할 수 없습니다."

    # pw
    if not password:
        return "비밀번호를 입력해주세요."

    if len(password) < 8 or \
        not any(char.isdigit() for char in password) or \
        not any(char.isupper() for char in password) or \
        not any(char in string.punctuation for char in password):
        return "비밀번호는 최소 8자 이상, 숫자와 대문자, 특수문자를 각각 하나 이상 포함해야 합니다."

    # nickname
    if not nickname:
        return "닉네임을 입력해주세요."

    if CustomUser.objects.filter(nickname=nickname).exists():
        return "이미 존재하는 닉네임입니다."
    
    if not (2 <= len(nickname) <= 20) or " " in nickname or not nickname.isalnum(): 
        return "닉네임은 2자 이상, 20자 이하로 입력해야 하며, 공백 또는 특수문자를 포함할 수 없습니다."
    
    # email
    if not email:
        return "이메일을 입력해주세요."

    if CustomUser.objects.filter(email=email).exists():
        return "이미 존재하는 이메일입니다."
    
    try:
        validate_email(email)
    except ValidationError:
        return "유효하지 않은 이메일 형식입니다."