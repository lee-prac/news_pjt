# Nozo Noews Project
Nozo 뉴스 프로젝트는 Django 프레임워크를 기반으로 뉴스 플랫폼의 기본 기능을 구현한 웹 애플리케이션 프로젝트 입니다.

## 프로젝트 개요
Nozo 뉴스는 RESTful API 방식을 사용하여 사용자 인증, 뉴스 열람, 댓글 작성, 좋아요 및 검색등과 같은 상호작용 기능을 제공하는 백엔드 API 입니다. 각 API endpoint는 HTTP 요청에 따라 필요한 데이터를 반환하며, 효율적인 데이터 처리를 목표로 하고 있습니다.

## 팀소개
- 팀명: Nozo
- 팀장: 이예지
- 팀원: 강지석, 이서원, 박현진, 차민승

## 개발일정
- 2024.09.11. ~ 2024.09.19.

## 개발환경
- Language: Python 3.10
- Framework: Django 4.2
- Database: SQLite, DjangoORM
- IDE: VSCode, PyCharm

## 주요기능
1. 회원관리
2. 뉴스관리
3. 댓글관리
4. 좋아요 및 북마크
5. 검색기능

### 1️⃣ 회원관리
- 회원가입: 사용자는 플랫폼에 가입하여 개인 계정을 생성할 수 있습니다.
  - Required: Username(unique), password, nickname(unique), email(unique),
  - Optional: Bio, Gender? 또 뭐더라
- 로그인 : 회원은 자신의 계정으로 로그인하여 서비스를 이용할 수 있습니다.
- 로그아웃 : 회원은 자신의 로그인 세션을 종료할 수 있습니다.
- 회원정보 수정 : 회원은 자신의 프로필 정보를 수정할 수 있습니다.
- 회원탈퇴 : 회원은 언제든지 계정을 삭제할 수 있으며, 탈퇴 시 계정은 비활성화로 전환됩니다.

- ------

 ###  2️⃣ 유저기능
  - 프로필 : 본인 또는 다른 유저의 프로필을 조회할 수 있습니다.
  - 작성한 게시물 조회 : 자신이 등록한 게시물을 조회 및 관리할 수 있습니다.
  - 찜한 게시물 조회 : 자신이 찜한 게시물을 조회 및 관리할 수 있습니다.

------

###  3️⃣ 뉴스관리
  - 작성 : 사용자는 글을 작성하여 플랫폼에 게시할 수 있습니다.
    - 필수 : 제목, 내용, 
    - 선택 : URL, 사진, 뭐더라
  - 수정 : 자신이 게시한 글의 내용을 수정할 수 있으며, 권한이 없는 사용자는 수정할 수 없습니다.
  - 삭제 : 자신이 게시한 글을 삭제할 수 있으며, 권한이 없는 사용자는 삭제할 수 없습니다.

------

###  4️⃣ 좋아요 및 북마크 북마크 하지 말까 그냥
  - 뉴스 좋아요 : 사용자는 뉴스를 좋아요할 수 잇음
    - 사용자는 자신 혹은 다른 유저가 좋아요 한 뉴스 목록을 조회할 수 있음
  - 댓글 좋아요 : 사용자는 댓글에도 좋아요를 누를 수 있음
    - 사용자는 자신이 좋아요 한 댓글 목록을 조회할 수 있음

------

###  5️⃣ 뉴스검색
  - 뉴스 검색 : 사용자는 제목, 내용 등을 기준으로 뉴스를 검색할 수 있음

------

##  API 명세서
|Index|기능|method type|API Path|Authorization|
|---|---|---|------|---|
|1|회원 가입|GET|/api/accounts/|all|
|2|회원 탈퇴|DELETE|/api/accounts/|user|
|3|로그인|POST|/api/accounts/login/|all|
|4|로그아웃|POST|/api/accounts/logout/|user|
||비밀번호 변경|PUT|/api/accounts/<str:username>/password/|user|
|5|프로필 조회|GET|/api/accounts/<str:username>/|all|
|6|프로필 수정|PUT|/api/accounts/<str:username>/|user|
|7|작성 글 목록|GET|/api/accounts/<str:username>/my_articles/|all|
|8|작성 댓글 목록|GET|/api/accounts/<str:username>/my_comments/|user|
|9|좋아요 글 목록|GET|/api/accounts/<str:username>/like_articles/|all|
|10|좋아요 댓글 목록|GET|/api/accounts/<str:username>/like_comments/|user|
|11|글 등록|POST|/api/articles/|user|
|12|최신글 목록|GET|/api/articles/|all|
|13|예전글 목록|GET|/api/articles/past/|all|
|13|인기글 목록|GET|/api/articles/like/|all|
|14|News 목록|GET|/api/articles/news/|all|
|14|ASK 목록|GET|/api/articles/ask/|all|
|15|Show 목록|GET|/api/articles/show/|all|
|15|글 상세|GET|/api/articles/<int:article_pk>/|all|
|15|글 수정|PUT|/api/articles/<int:article_pk>/|user|
|15|글 삭제|DELETE|/api/articles/<int:article_pk>/|user|
|15|댓글 목록|GET|/api/articles/comments/|all|
|15|댓글 상세|GET|/api/articles/<int:comment_pk>/|all|
|15|댓글 수정|PUT|/api/articles/<int:comment_pk>/|user|
|15|댓글 삭제|DELETE|/api/articles/<int:comment_pk>/|user|
|15|글 좋아요|POST|/api/articles/<int:article_pk>/like/|user|
|15|글 좋아요 취소|DELETE|/api/articles/<int:article_pk>/like/|user|
|15|댓글 좋아요|POST|/api/articles/<int:comment_pk>/like/|user|
|15|댓글 좋아요 취소|DELETE|/api/articles/<int:comment_pk>/like/|user|
|15|글 검색|GET|/api/articles/search/|all|

------

## Wireframe

![Wireframe](https://github.com/user-attachments/assets/700d5306-2745-4eb6-b1ae-4bc477ec81e4)

------

## ERD

![ERD](https://github.com/user-attachments/assets/dfcde3fa-7be7-4c8e-8f6d-bea71f799900)
