from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'comments', CommentViewSet)


# URL 패턴 정의

app_name ="news"
urlpatterns = [
    path('', include(router.urls)),  # 기본 라우팅 
    path('news/', NewsViewSet.as_view({'get': 'list'}), name='news_list'), 
]
