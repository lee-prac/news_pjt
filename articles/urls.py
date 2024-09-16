from django.urls import path
from . import views

app_name="articles"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article"),
    path("category/", views.CategoryListView.as_view()),
    path("<int:pk>/", views.ArticleDetailView.as_view()),
]

