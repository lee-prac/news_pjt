from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer



class ArticleListView(ListAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            return Article.objects.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            ) 
        return Article.objects.all()

    def post(self, request): # 글 작성 / 로그인 필요
        title = request.data.get('title')
        content = request.data.get('content')
        image = request.data.get('image')
        category_id_text = request.data.get('category')
        article = Article.objects.create(
            title = title,
            content = content,
            image = image,
            category_id = category_id_text,
        )
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # def get(self, request):
    #     products = Article.objects.all()
    #     serializer = ArticleSerializer(products, many=True)
    #     return Response(serializer.data)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer = ArticleSerializer(Article, many=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


