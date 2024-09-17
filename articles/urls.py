from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"comments", views.CommentViewSet, basename="comment")

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article"),
    path("category/", views.CategoryListView.as_view()),
    path("<int:pk>/", views.ArticleDetailView.as_view()),
    path("news/", views.NewsViewSet.as_view({"get": "list"}), name="news_list"),
    path(
        "news/<int:pk>/",
        views.NewsViewSet.as_view({"get": "retrieve"}),
        name="news_detail",
    ),
    path("", include(router.urls)),
]
