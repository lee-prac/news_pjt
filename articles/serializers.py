from rest_framework import serializers
from .models import Article, Category

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = CategorySerializer(instance.category).data
        return ret
