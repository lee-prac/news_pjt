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

    # pw_change
def validate_password_change(new_password, old_password, user):
    if not new_password:
        return "비밀번호를 입력해주세요."

    if len(new_password) < 8 or \
            not any(char.isdigit() for char in new_password) or \
            not any(char.isupper() for char in new_password) or \
            not any(char in string.punctuation for char in new_password):
        return "비밀번호는 최소 8자 이상, 숫자와 대문자, 특수문자를 각각 하나 이상 포함해야 합니다."

    if old_password == new_password:
        return "새 비밀번호는 기존 비밀번호와 달라야 합니다."

    if not user.check_password(old_password):
        return "기존 비밀번호가 틀렸습니다."
