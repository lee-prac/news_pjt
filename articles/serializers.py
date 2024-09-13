from rest_framework import serializers
from accounts.models import CustomUser
from articles.models import Article


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["nickname", "email"]


# Create, Update
class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "content", "url"]

    @staticmethod
    def get_queryset():
        return Article.objects.all().only("title", "content", "url")


# Read-list
class ArticleListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ["id", "title", "url", "content", "author"]  # id는 확인용

    @staticmethod
    def get_queryset():
        return (
            Article.objects.all()
            .only("id", "title", "url", "content", "author")
            .select_related("author")
        )


# Read-detail
class ArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ["id", "author", "title", "created_at", "updated_at", "content"]

    @staticmethod
    def get_queryset():
        return (
            Article.objects.all()
            .only("id", "author", "title", "created_at", "updated_at", "content")
            .select_related("author")
        )
