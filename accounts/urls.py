from django.urls import path
from .views import SignupView

urlpatterns = [
    # 회원가입 경로
    path("signup/", SignupView.as_view(), name="signup"),
]
