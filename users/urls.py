from django.urls import path
from . import views

urlpatterns = [
    path("<str:user_id>/", views.ProfileView.as_view()),
    path("<str:nickname>/articles/", views.ArticlesView.as_view()),
    path("<str:nickname>/comments/", views.CommentsView.as_view()),
    path("<str:nickname>/like_articles/", views.LikeArticlesView.as_view()),
    path("<str:nickname>/like_comments/", views.LikeCommentsView.as_view()),
]
