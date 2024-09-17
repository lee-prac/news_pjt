from django.db import models
from django.conf import settings
from django.utils import timezone

# 뉴스 모델
class News(models.Model):
    title = models.CharField(max_length=255)  # 뉴스 제목 길이를 늘림
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 좋아요 기능 (Many-to-Many 관계)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_news', blank=True)

    # 즐겨찾기 기능 (Many-to-Many 관계)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_news', blank=True)

    # 포인트 계산 함수
    def calculate_points(self):
        # 뉴스가 게시된 날짜로부터 경과 일 수에 따라 포인트 계산
        days_since_pub = (timezone.now() - self.created_at).days
        points = self.comments.count() * 3 + self.likes.count() * 1 - days_since_pub * 5
        return points


# 댓글 모델
class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 댓글 좋아요와 즐겨찾기 기능
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmarked_comments', blank=True)
