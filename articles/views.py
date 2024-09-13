from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Article
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateUpdateSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Article.objects.all()  # 기본 쿼리셋

    # CRUD에 따른 시리얼라이저 반환
    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ArticleCreateUpdateSerializer  # Create, Update
        elif self.action == "list":
            return ArticleListSerializer  # Read-list
        elif self.action in ["retrieve", "destroy"]:
            return ArticleDetailSerializer  # Read-detail, Delete

    def get_queryset(self):
        serializer_type = self.get_serializer_class()
        return serializer_type.get_queryset()  # 각 시리얼라이저의 쿼리셋 호출

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 작성자=현재유저 자동 설정

    def update(self, request, *args, **kwargs):
        article = self.get_object()
        if article.author != request.user:
            raise PermissionDenied("본인의 글만 수정할 수 있습니다!")
        kwargs["partial"] = True  # 일부만 수정하기 허용
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # if instance.author != self.request.user:
        #     raise PermissionDenied("본인의 글만 삭제할 수 있습니다!")
        instance.delete()
