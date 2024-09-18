from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Article, Category, Comment, News
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
    CategorySerializer,
    CommentSerializer,
    NewsSerializer,
)

from rest_framework.decorators import action
import requests
from bs4 import BeautifulSoup


class ArticleListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NewsSerializer

    def get_queryset(self):
        search = self.request.query_params.get("search", None)
        queryset = News.objects.all()
        if search:
            queryset = News.objects.filter(Q(title__icontains=search))
        return queryset

    # 결과반환 역할
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists() and "search" in request.query_params:
            return Response(
                data={"detail": "검색 결과가 없습니다!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_news_queryset = self.crawl_news()
        all_news = queryset.union(new_news_queryset)

        # 크롤링한 뉴스 목록을 JSON 형식으로 반환
        serializer = NewsSerializer(all_news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 크롤링 역할
    def crawl_news(self):
        url = "https://www.bbc.com/news/technology"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        try:
            # BBC 뉴스 페이지 요청
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # HTML 파싱
            soup = BeautifulSoup(response.text, "html.parser")

            # 크롤링된 뉴스 목록을 담을 리스트
            new_news_list = []

            # h2 태그로 뉴스 제목 추출, 링크는 상위 a 태그에서 추출
            for item in soup.select("h2"):
                title = item.get_text(strip=True)
                link_tag = item.find_parent("a")  # 상위 a 태그에서 링크 찾기

                # 링크가 있으면 링크 추출, 없으면 '링크 없음'으로 처리
                if link_tag and "href" in link_tag.attrs:
                    link = link_tag["href"]
                    # 상대 경로 처리
                    if not link.startswith("http"):
                        link = f"https://www.bbc.com{link}"
                else:
                    link = "링크 없음"

                # 새뉴스만 db 저장
                if not News.objects.filter(title=title).exists():
                    news = News.objects.create(title=title, link=link)
                    new_news_list.append(news)

            return News.objects.filter(id__in=[news.id for news in new_news_list])

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"뉴스 크롤링 실패: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # # 뉴스에 대한 댓글 보여주기 API - 로그인 없이 가능
    # @action(detail=True, methods=["get"])
    # def comments(self, request, pk=None):
    #     news = self.get_object()
    #     comments = news.comments.all()
    #     serializer = CommentSerializer(comments, many=True)
    #     return Response(serializer.data)
    #
    # # 뉴스에 댓글 작성하기 API - 로그인 필요 없음
    # @action(detail=True, methods=["post"])
    # def add_comment(self, request, pk=None):
    #     news = self.get_object()
    #     data = request.data.copy()
    #     data["news"] = news.id
    #     serializer = CommentSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save(
    #             author=request.user if request.user.is_authenticated else None
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 모델의 ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # list() 메서드 오버라이드하여 빈 리스트 처리
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_200_OK)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied("본인의 댓글만 수정할 수 있습니다!")
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("본인의 댓글만 삭제할 수 있습니다!")
        instance.delete()
