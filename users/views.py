from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from accounts.models import CustomUser
from .serializers import ProfileSerializer, ProfileUpdateSerializer
from .validators import validate_user_data, validate_password_change



# 프로필
class ProfileView(APIView):
    # 프로필 조회는 권한 없이도 가능, 조회가 목적이 아니면 기본 권한 설정 적용
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 조회
    def get(self, request, user_id):
        user = CustomUser.objects.get(user_id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    # 수정
    def put(self, request, user_id):
        # 현재 로그인된 사용자가 본인인지 확인
        if request.user.user_id != user_id:
            return Response({'detail': '본인의 프로필만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 데이터 유효성 검사
        rlt_message = validate_user_data(request.data, request.user)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 조회
        user = CustomUser.objects.get(user_id=user_id)

        # Serializer로 데이터 업데이트
        serializer = ProfileUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        rlt_message = validate_password_change(new_password, old_password, request.user)
        if rlt_message:
            return Response({"message": rlt_message}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 변경 처리
        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
