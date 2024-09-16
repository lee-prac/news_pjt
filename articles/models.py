from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(TimeStampedModel):
    title = models.CharField(max_length=25)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/image/', null=True, blank=True)
    url = models.URLField(blank=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_articles",  # 필요없으면 삭제하자
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='articles',
        null=True,
        blank=True
        )
    created_date = models.ForeignKey(auto_now_add=True)
    update_date = models.ForeignKey(update_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-id"]  # 저장할 때 역순으로 정렬

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)


