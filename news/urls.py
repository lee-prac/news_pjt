from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, CommentViewSet, UserViewSet, NaverNewsCrawlAPIView

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)

# URL 패턴 정의
urlpatterns = [
    path('', include(router.urls)),  # 기본 라우팅 포함
    path('news/crawl/', NaverNewsCrawlAPIView.as_view(), name='crawl_news'),  # 네이버 뉴스 크롤링 API 경로
]
