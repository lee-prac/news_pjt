from rest_framework import serializers
from .models import News, Comment
from django.contrib.auth import get_user_model  # 사용자 모델 가져오기

User = get_user_model()  # 커스텀 사용자 모델

# 사용자 직렬화
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# 댓글 직렬화
class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    author = UserSerializer(read_only=True)  # author를 UserSerializer로 연결

    class Meta:
        model = Comment
        fields = ['id', 'news', 'author', 'content', 'created_at', 'likes_count']


# 뉴스 직렬화
class NewsSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    points = serializers.IntegerField(source='calculate_points', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)  # 뉴스와 관련된 댓글을 직렬화

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'comments_count', 'likes_count', 'points', 'comments']
