from django.core.management.base import BaseCommand
from django_seed import Seed
from articles.models import Article, Category, Comment, ArticleLike, CommentLike
from django.contrib.auth import get_user_model
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # 유저: 10명 생성!
        seeder.add_entity(
            User,
            10,
            {
                "user_id": lambda x: seeder.faker.user_name(),
                "email": lambda x: seeder.faker.email(),
                "password": lambda x: seeder.faker.password(),
                "nickname": lambda x: seeder.faker.first_name(),
            },
        )

        # 카테고리: News, Ask, Show 고정
        category_names = ["News", "Ask", "Show"]
        for name in category_names:
            Category.objects.get_or_create(name=name)

        users = User.objects.all()[:10]

        # Article: 총 50개 생성!
        seeder.add_entity(
            Article,
            50,
            {
                "title": lambda x: seeder.faker.sentence(),
                "content": lambda x: seeder.faker.text(),
                "category": lambda x: Category.objects.get(
                    name=random.choice(category_names)
                ),
                "author": lambda x: random.choice(users),
                # 날짜: 최근 일주일 중 하루
                "created_at": lambda x: timezone.now()
                - timedelta(days=random.randint(0, 6)),
            },
        )

        # Comment: 총 150개 (댓글, 대댓글)
        seeder.add_entity(
            Comment,
            150,
            {
                "article": lambda x: random.choice(Article.objects.all()),
                "content": lambda x: seeder.faker.text(),
                "author": lambda x: random.choice(users),
                "parent": lambda x: random.choice(
                    [None] + list(Comment.objects.filter(parent=None))
                ),
            },
        )

        # 게시글 좋아요: 총 200개
        seeder.add_entity(
            ArticleLike,
            200,
            {
                "article": lambda x: random.choice(Article.objects.all()),
                "user": lambda x: random.choice(users),
            },
        )
        # 댓글 좋아요: 총 500개
        seeder.add_entity(
            CommentLike,
            500,
            {
                "comment": lambda x: random.choice(Comment.objects.all()),
                "user": lambda x: random.choice(users),
            },
        )

        seeder.execute()

        print("\n\n" + "-" * 50)
        print(self.style.SUCCESS("방금 뜬 WARNING은 장고 기본 테이블 때문이니까 신경쓰지 마세요!!!!\n"))
        print(self.style.SUCCESS("유저 10, 게시글 50, 댓글 150, 글좋아요 200, 댓글좋아요 500 생성 성공!!\n"))

        # 생성된 유저들의 nickname 출력하기 (쓸거같음)
        created_users = User.objects.all()[:10]
        nicknames = [user.nickname for user in created_users]
        self.stdout.write(self.style.SUCCESS(f"닉네임 10개: {', '.join(nicknames)}"))
