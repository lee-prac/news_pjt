from django.urls import path
from . import views

urlpatterns = [
    path("<str:user_id>/", views.ProfileView.as_view()),
    path("password/", views.PasswordChangeView.as_view()),
]
