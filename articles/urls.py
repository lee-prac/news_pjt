from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"comments", views.CommentViewSet, basename="comment")
router.register(r"news", views.NewsViewSet, basename="news")

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article"),
    path("category/", views.CategoryListView.as_view()),
    path("<int:pk>/", views.ArticleDetailView.as_view()),
    path("", include(router.urls)),  # 뉴스랑 댓글
    path("<int:article_pk>/like/", views.ArticleLikeAPIView.as_view()),
    path("comments/<int:comment_pk>/like/", views.CommentLikeAPIView.as_view()),
    path("popular/", views.PopularArticleView.as_view()),  # 인기순(==포인트순)
]
