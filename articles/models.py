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
        to='Category',
        on_delete=models.CASCADE,
        related_name='articles',
        null=True,
        blank=True
        )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-id"]  # 저장할 때 역순으로 정렬

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

# 댓글 모델 (Comment)
class Comment(TimeStampedModel):
    # 댓글이 달린 뉴스 (ForeignKey를 통해 News 모델과 연결, 해당 뉴스가 삭제되면 댓글도 삭제됨)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    
    # 댓글 작성자 (ForeignKey를 통해 사용자 모델과 연결)
    # 로그인 없이도 댓글 작성 가능
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE)
    
    # 댓글 내용 (긴 텍스트 저장을 위해 TextField 사용)
    content = models.TextField()


    # 객체의 문자열 표현을 댓글 내용의 일부로 반환
    def __str__(self):
        return self.content[:20]

