from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("withdraw/", views.WithdrawView.as_view()),
    path("password/", views.PasswordChangeView.as_view()),
]
