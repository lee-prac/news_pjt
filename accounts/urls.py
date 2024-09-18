from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('delete/',views.DeleteAPIView.as_view(), name="delete"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
