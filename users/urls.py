from django.urls import path
from . import views

urlpatterns = [
    path("<str:user_id>/", views.ProfileView.as_view()),
    path("password/", views.PasswordChangeView.as_view()),
    path("<str:nickname>/my_articles/", views.ArticlesView.as_view()),
    path("<str:nickname>/my_comments/", views.CommentsView.as_view()),
    path("<str:nickname>/like_articles/", views.LikeArticlesView.as_view()),
    path("<str:nickname>/like_comments/", views.LikeCommentsView.as_view()),
]
