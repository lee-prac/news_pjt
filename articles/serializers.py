from rest_framework import serializers
from .models import Article, Category, Comment, News
from django.utils import timezone


# 댓글 직렬화 (CommentSerializer)
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.nickname", read_only=True)
    replies = serializers.SerializerMethodField()  # 대댓글 직렬화
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False,
    )  # 대댓글을 위한 필드 "parent" == "댓글pk"

    comment_likes_count = serializers.IntegerField(
        source="comment_likes.count", read_only=True
    )  # 댓글 좋아요 수

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "parent", "replies", "comment_likes_count"]
        read_only_fields = ("article", "author")

    def get_replies(self, obj):
        replies = obj.replies.all()  # 미리 prefetch된 replies를 사용
        return CommentSerializer(replies, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.nickname", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "author", "created_at", "comments_count", "points"]

    # 게시글 포인트
    points = serializers.SerializerMethodField()

    def get_points(self, obj):
        # 게시일 기준 하루마다 -5 point  # 저녁에 작성한 사람 안억울하게 초단위로 계산하기
        article_age = timezone.now() - obj.created_at
        article_age_days = article_age.total_seconds() // (24 * 60 * 60)
        time_points = int(-5 * article_age_days)

        comment_points = obj.comments.count() * 3  # 댓글 수 +3 point

        like_points = obj.article_likes.count()  # 좋아요 수 +1 point

        total_points = time_points + comment_points + like_points
        return total_points if total_points > 0 else 0


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.nickname", read_only=True)
    article_likes_count = serializers.IntegerField(
        source="article_likes.count", read_only=True
    )  # 게시글 좋아요 수
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["author"]

    # 카테고리를 "id" 가 아닌 "카테고리이름" 으로 보여주기.
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = instance.category.name
        return ret


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "link", "crawled_at"]
