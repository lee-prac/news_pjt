from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from django.db.models import Q
# from rest_framework.pagination import PageNumberPagination
from .models import Article
from .serializers import ArticleSerializer


class ProductListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search:
            return Article.objects.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            ) 
        return Article.objects.all()

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        image = request.data.get('image')
        product = Article.objects.create(
            title = title,
            content = content,
            image = image,
        )
        serializer = ArticleSerializer(product)
        return Response(serializer.data)

    # def get(self, request):
    #     products = Article.objects.all()
    #     serializer = ArticleSerializer(products, many=True)
    #     return Response(serializer.data)


class ProductListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer = ArticleSerializer(Article, many=True)
    permission_classes = [IsAuthenticatedOrReadOnly]