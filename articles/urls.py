from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter()
router.register(r"", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


# api/articles/
# GET: 목록 / POST: 생성

# api/articles/<pk>/
# GET: 상제 / PUT: 수정 / DELETE: 삭제
