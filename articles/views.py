from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


class ArticleListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

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

        article = Article.objects.create(
            title=title,
            content=content,
            image=image,
            category_id=category_id_text,
            author=request.user,  # 요청한 사용자를 author로 설정
        )
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
