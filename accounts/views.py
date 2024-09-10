from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from .models import User
from .validators import validate_user_data

# Create your views here.
class UserCreateView(APIView):
    def post(self, request):
        result_message = validate_user_data(request.data)
        if result_message is not None:
            return Response({"message": result_message},status=400)

        user = User.objects.create_user(**request.data)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
class UserLoginView(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        print(username,password)
        