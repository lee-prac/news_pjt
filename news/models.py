from django.db import models
from django.conf import settings

# 뉴스 모델 (News)
class News(models.Model):
    # 뉴스 제목 (최대 길이 255자)
    title = models.CharField(max_length=255)
    
    # 뉴스 내용 (긴 텍스트 저장을 위해 TextField 사용)
    content = models.TextField()
    
    # 뉴스가 생성된 시간 (자동으로 생성 시각이 입력됨)
    created_at = models.DateTimeField(auto_now_add=True)

    # 객체의 문자열 표현을 뉴스 제목으로 반환
    def __str__(self):
        return self.title


# 북마크 모델 (Bookmark)
class Bookmark(models.Model):
    # 특정 뉴스에 대한 북마크
    news = models.ForeignKey(News, related_name='bookmarks', on_delete=models.CASCADE)
    
    # 북마크한 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 북마크한 시간
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 동일한 사용자가 동일한 뉴스에 여러 번 북마크할 수 없도록 unique 설정
        unique_together = ('news', 'user')

    def __str__(self):
        return f"{self.user} bookmarked {self.news.title}"

# 댓글 모델 (Comment)
class Comment(models.Model):
    # 댓글이 달린 뉴스 (ForeignKey를 통해 News 모델과 연결, 해당 뉴스가 삭제되면 댓글도 삭제됨)
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    
    # 댓글 작성자 (ForeignKey를 통해 사용자 모델과 연결)
    # 로그인 없이도 댓글 작성 가능
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE)
    
    # 댓글 내용 (긴 텍스트 저장을 위해 TextField 사용)
    content = models.TextField()
    
    # 댓글이 작성된 시간 (자동으로 작성 시각이 입력됨)
    created_at = models.DateTimeField(auto_now_add=True)


    # 객체의 문자열 표현을 댓글 내용의 일부로 반환
    def __str__(self):
        return self.content[:20]
