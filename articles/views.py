from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Article, Category
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    CategorySerializer,
)
from django.shortcuts import get_object_or_404


class ArticleListView(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        search = self.request.query_params.get("search")
        if search:
            return Article.objects.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        return Article.objects.all()

    def post(self, request):  # 글 작성 / 로그인 필요
        title = request.data.get("title")
        content = request.data.get("content")
        image = request.data.get("image")
        category_id_text = request.data.get("category")

        # 500에러 억울하니까 예외 처리 해줄게요!
        if not title:
            return Response(
                data={"message": "제목은 필수 입력란 입니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not content:
            return Response(
                data={"message": "내용은 필수 입력란 입니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            category = Category.objects.get(id=category_id_text)
        except Category.DoesNotExist:
            raise ValidationError({"category": "그런 카테고리는 없습니다!"})

        article = Article.objects.create(
            title=title,
            content=content,
            image=image,
            category_id=category_id_text,
            author=request.user,  # 요청한 사용자를 author로 설정
        )
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if article.author != request.user:
            return Response(
                data={"detail": "본인의 글만 수정할 수 있습니다!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if article.author != request.user:
            return Response(
                data={"detail": "본인의 글만 삭제할 수 있습니다!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
