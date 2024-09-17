from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import CustomUser
from .serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = CustomUser.objects.get(user_id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
