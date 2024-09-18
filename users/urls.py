from django.urls import path
from . import views

urlpatterns = [
    path("<str:user_id>/", views.ProfileView.as_view()),
    path("password/", views.PasswordChangeView.as_view()),
    path("<str:nickname>/my_articles/", views.MyArticlesView.as_view()),
#     path("<str:user_id>/my_comments/", views.MyCommentsView.as_view()),
#     path("<str:user_id>/like_articles/", views.LikeArticlesView.as_view()),
#     path("<str:user_id>/like_comments/", views.LikeCommentsView.as_view()),
]
