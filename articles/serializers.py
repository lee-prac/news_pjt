from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "author", "created_at"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    # author를 "id" 가 아닌 "user_id" 로 보여주기.
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["author"]

    # 카테고리를 "id" 가 아닌 "카테고리이름" 으로 보여주기.
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = CategorySerializer(instance.category).data
        return ret
