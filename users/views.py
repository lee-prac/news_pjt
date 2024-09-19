from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from accounts.models import CustomUser
from articles.models import Article, Comment
from .serializers import ProfileSerializer, ProfileUpdateSerializer
from articles.serializers import ArticleListSerializer, CommentSerializer
from .validators import validate_user_data


# 프로필
class ProfileView(APIView):
    # 프로필 조회는 권한 없이도 가능, 조회가 목적이 아니면 기본 권한 설정 적용
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 조회
    def get(self, request, user_id):
        user = CustomUser.objects.get(user_id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    # 수정
    def put(self, request, user_id):
        # 현재 로그인된 사용자가 본인인지 확인
        if request.user.user_id != user_id:
            return Response({'detail': '본인의 프로필만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 데이터 유효성 검사
        rlt_message = validate_user_data(request.data)
        if rlt_message is not None:
            return Response({"message": rlt_message}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 조회
        user = CustomUser.objects.get(user_id=user_id)

        # Serializer로 데이터 업데이트
        serializer = ProfileUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticlesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, nickname):
        try:
            author = CustomUser.objects.get(nickname=nickname)
        except CustomUser.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        articles = Article.objects.filter(author=author)

        if not articles.exists():
            return Response({"message": "작성한 글이 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsView(APIView):
    def get(self, request, nickname):
        try:
            author = CustomUser.objects.get(nickname=nickname)
        except CustomUser.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(author=author)

        if not comments.exists():
            return Response({"message": "작성한 댓글이 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeArticlesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, nickname):
        try:
            user = CustomUser.objects.get(nickname=nickname)
        except CustomUser.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        liked_articles = Article.objects.filter(article_likes__user=user)

        if not liked_articles.exists():
            return Response({"message": "좋아요한 글이 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = ArticleListSerializer(liked_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeCommentsView(APIView):
    def get(self, request, nickname):
        try:
            user = CustomUser.objects.get(nickname=nickname)
        except CustomUser.DoesNotExist:
            return Response({"message": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        liked_comments = Comment.objects.filter(comment_likes__user=user)

        if not liked_comments.exists():
            return Response({"message": "좋아요한 댓글이 없습니다."}, status=status.HTTP_204_NO_CONTENT)

        serializer = CommentSerializer(liked_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)