from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .validators import validate_user_data
from .serializers import SignupSerializer

class SignupView(APIView):
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

        serializer = SignupSerializer(user)
        return Response(serializer.data)