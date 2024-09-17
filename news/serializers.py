from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import News, Comment    # 모델 임포트

User = get_user_model()

# 사용자 직렬화 (UserSerializer)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 댓글 직렬화 (CommentSerializer)
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'news', 'author', 'content', 'created_at']

# 뉴스 직렬화 (NewsSerializer)
class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'comments']
