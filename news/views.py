from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer, UserSerializer
import requests
from bs4 import BeautifulSoup
from django.db.models import Q

User = get_user_model()  # 사용자 모델 가져오기

# 뉴스 모델의 ViewSet
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    # 포인트가 많은 순으로 뉴스 정렬 API
    @action(detail=False, methods=['get'])
    def sorted_news(self, request):
        news_list = News.objects.all()
        # 포인트 기준으로 내림차순 정렬
        sorted_news = sorted(news_list, key=lambda news: news.calculate_points(), reverse=True)
        serializer = self.get_serializer(sorted_news, many=True)
        return Response(serializer.data)

    # 뉴스 좋아요 API
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        news = self.get_object()
        news.likes.add(request.user)
        return Response({'status': 'news liked'})

    # 뉴스 북마크 API
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        news = self.get_object()
        news.bookmarks.add(request.user)
        return Response({'status': 'news bookmarked'})

    # 사용자가 좋아요한 뉴스 목록 API
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def liked_news(self, request):
        liked_news = News.objects.filter(likes=request.user)
        serializer = self.get_serializer(liked_news, many=True)
        return Response(serializer.data)

    # 사용자가 북마크한 뉴스 목록 API
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def bookmarked_news(self, request):
        bookmarked_news = News.objects.filter(bookmarks=request.user)
        serializer = self.get_serializer(bookmarked_news, many=True)
        return Response(serializer.data)

    # 뉴스 검색 API
    @action(detail=False, methods=['get'])
    def search_news(self, request):
        query = request.query_params.get('q', None)
        if query:
            news_list = News.objects.filter(Q(title__icontains=query) | Q(content__icontains(query)))
            serializer = self.get_serializer(news_list, many=True)
            return Response(serializer.data)
        return Response({"detail": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 뉴스에 대한 댓글 보여주기 API
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        news = self.get_object()
        comments = news.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 뉴스에 댓글 작성하기 API
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        news = self.get_object()
        data = request.data.copy()
        data['news'] = news.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 모델의 ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # 댓글 좋아요 API
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        comment.likes.add(request.user)
        return Response({'status': 'comment liked'})

    # 댓글 북마크 API
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        comment = self.get_object()
        comment.bookmarks.add(request.user)
        return Response({'status': 'comment bookmarked'})

    # 사용자가 좋아요한 댓글 목록 API
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def liked_comments(self, request):
        liked_comments = Comment.objects.filter(likes=request.user)
        serializer = self.get_serializer(liked_comments, many=True)
        return Response(serializer.data)

    # 사용자가 북마크한 댓글 목록 API
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def bookmarked_comments(self, request):
        bookmarked_comments = Comment.objects.filter(bookmarks=request.user)
        serializer = self.get_serializer(bookmarked_comments, many=True)
        return Response(serializer.data)


# 네이버 뉴스 크롤링을 위한 API View
class NaverNewsCrawlAPIView(APIView):
    """
    네이버 뉴스 페이지에서 최신 뉴스를 크롤링하는 API View
    """
    def get(self, request, *args, **kwargs):
        # 네이버 뉴스 페이지 URL
        url = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001'

        # 페이지 요청
        try:
            response = requests.get(url, timeout=5)  # 타임아웃 추가
        except requests.exceptions.RequestException as e:
            return Response({"error": f"네이버 뉴스 페이지 요청에 실패했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 요청이 성공적인 경우
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 뉴스 제목과 링크 추출
            news_list = []
            for item in soup.select('.list_body .newsflash_body .type06_headline li dl dt a'):
                title = item.get_text(strip=True)
                link = item['href']
                news_list.append({'title': title, 'link': link})

            # 크롤링한 데이터를 JSON 형식으로 반환
            return Response(news_list, status=status.HTTP_200_OK)
        else:
            # 오류 발생 시
            return Response({"error": "네이버 뉴스 페이지를 가져오지 못했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 사용자 모델의 ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
