# Nozo News Project
Nozo 뉴스 프로젝트는 Django 프레임워크를 기반으로 뉴스 플랫폼의 기본 기능을 구현한 웹 애플리케이션 프로젝트 입니다.

## 프로젝트 개요
Nozo 뉴스는 RESTful API 방식을 사용하여 사용자 인증, 뉴스 열람, 댓글 작성, 좋아요 및 검색등과 같은 상호작용 기능을 제공하는 백엔드 API 입니다. 각 API endpoint는 HTTP 요청에 따라 필요한 데이터를 반환하며, 효율적인 데이터 처리를 목표로 하고 있습니다.

## 팀소개
- 팀명: Nozo
- 팀장: 이예지
- 팀원: 강지석, 이서원, 박현진, 차민승

## 개발일정
- 2024.09.11 ~ 2024.09.19

## 개발환경
- Language: Python 3.10
- Framework: Django 4.2
- Database: SQLite, DjangoORM
- IDE: VSCode, PyCharm

## 주요기능
1. 회원 기능
2. 유저 기능
3. 게시글 기능
4. 댓글 기능
5. 좋아요 기능
6. 검색 기능

### 1️⃣ 회원 기능
- 회원가입: 사용자는 플랫폼에 가입하여 개인 계정을 생성할 수 있습니다.
  - Required: user_id(unique), password, nickname(unique), email(unique)
  - Optional: bio
- 로그인 : 회원은 자신의 계정으로 로그인하여 서비스를 이용할 수 있습니다.
- 로그아웃 : 회원은 자신의 로그인 세션을 종료할 수 있습니다.
- 회원탈퇴 : 회원은 언제든지 계정을 삭제할 수 있으며, 탈퇴 시 계정은 비활성화로 전환됩니다.
- 비밀번호 변경 : 회원은 자신의 비밀번호를 변경할 수 있습니다.
------

 ###  2️⃣ 유저 기능
  - 프로필 : 본인 또는 다른 유저의 프로필을 조회할 수 있습니다.
  - 회원 정보 수정 : 회원은 자신의 프로필 정보를 수정할 수 있습니다.
  - 작성한 게시글 조회 : 특정 유저가 등록한 게시물을 조회할 수 있습니다.
  - 작성한 댓글 조회 : 자신이 등록한 댓글을 조회할 수 있습니다.
  - 좋아요를 남긴 게시글 조회 : 특정 유저가 좋아요를 남긴 게시물을 조회할 수 있습니다.
  - 좋아요를 남긴 댓글 조회 : 자신이 좋아요를 남긴 댓글을 조회할 수 있습니다.

------

###  3️⃣ 게시글 기능
  - 작성 : 사용자는 글을 작성하여 플랫폼에 게시할 수 있습니다.
    - 게시글 구성 : 제목, 내용, 사진, 카테고리, 작성자, URL
    - 작성 시 입력 사항
        - 필수 : 제목, 내용, 
        - 선택 : URL, 사진, 카테고리
  - 수정 : 자신이 게시한 글의 내용을 수정할 수 있으며, 권한이 없는 사용자는 수정할 수 없습니다.
  - 삭제 : 자신이 게시한 글을 삭제할 수 있으며, 권한이 없는 사용자는 삭제할 수 없습니다.
  - 정렬 : 최신순, 인기순, 

------

###  4️⃣ 댓글 기능
  - 댓글 등록 : 사용자는 각 카테고리에 있는 게시글에 댓글을 등록할 수 있습니다.
  - 댓글 조회 : 사용자는 모든 댓글 목록을 최신 순으로 조회할 수 있습니다.
  - 대댓글 등록 : 사용자는 게시글의 댓글에 댓글을 등록할 수 있습니다

------

###  5️⃣ 좋아요 기능
  - 게시글 좋아요 : 사용자는 뉴스를 좋아요를 남길 수 있습니다.
    - 사용자는 자신 혹은 다른 유저가 좋아요를 남긴 뉴스 목록을 조회할 수 있습니다.
  - 댓글 좋아요 : 사용자는 댓글에도 좋아요를 남길 수 있습니다.
    - 사용자는 자신이 좋아요 한 댓글 목록을 조회할 수 있습니다.

------

###  6️⃣ 조회 및 검색 기능
  - 목록 : 사용자는 특정 사이트에서 크롤링된 뉴스를 조회할 수 있습니다.
  - 상세 조회 : 사용자는 PK를 통해 특정 뉴스를 조회할 수 있으며, URL을 클릭하면 해당 뉴스로 이동할 수 있습니다.
  - 검색 : 사용자는 특정 키워드를 통해, 해당 단어가 제목에 포함된 뉴스를 검색할 수 있습니다.
  - - 정렬: 사용자는 특정 경로를 통해 원하는 목록을 조회할 수 있습니다.
- 최신글: 최신에 작성된 순서로 정렬된 목록을 조회할 수 있습니다.
- 이전글: 날짜를 검색하여 해당 날짜에 작성된 글 목록을 조회할 수 있습니다.
- 카테고리글: 특정 카테고리에 해당하는 글만을 필터링하여 조회할 수 있습니다.
- 인기글: 포인트 순으로 정렬된 목록을 조회할 수 있습니다.
- 정렬 : 사용자는 특정 경로를 통해 원하는 목록을 조회할 수 있습니다.
  - 최신글 : 최신에 작성된 순서로 정렬된 목록을 조회할 수 있습니다.
  - 이전글: 날짜를 검색하여 해당 날짜에 작성된 글 목록을 조회할 수 있습니다.
  - 카테고리별 조회: 특정 카테고리에 해당하는 글만을 필터링하여 조회할 수 있습니다.
  - 인기글: 포인트 순으로 정렬된 목록을 조회할 수 있습니다.
    - 날짜가 하루 지날때 마다 -5 Point, 댓글 하나당 +3 Point, 좋아요 하나당 +1 Point

------

##  API 명세서
|Index|기능|method type|API Path|Authorization|
|---|---|---|------|---|
|1|회원 가입|GET|/api/accounts/signup/|all|
|2|회원 탈퇴|DELETE|/api/accounts/withdraw/|user|
|3|로그인|POST|/api/accounts/login/|all|
|4|로그아웃|POST|/api/accounts/logout/|user|
|5|비밀번호 변경|PUT|/api/accounts/password/|user|
|6|프로필 조회|GET|/api/users/<str:user_id>/|all|
|7|프로필 수정|PUT|/api/users/<str:user_id>/|user|
|8|작성 글 목록|GET|/api/users/<str:nickname>/articles/|all|
|9|작성 댓글 목록|GET|/api/users/<str:nickname>/comments/|user|
|10|좋아요 글 목록|GET|/api/users/<str:nickname>/like_articles/|all|
|11|좋아요 댓글 목록|GET|/api/users/<str:nickname>/like_comments/|user|
|12|게시글 목록|GET|/api/articles/|all|
|13|게시글 생성|POST|/api/articles/|user|
|14|글 상세|GET|/api/articles/<int:article_pk>/|all|
|15|글 수정|PUT|/api/articles/<int:article_pk>/|user|
|16|글 삭제|DELETE|/api/articles/<int:article_pk>/|user|
|17|댓글 목록|GET|/api/articles/comments/|all|
|18|댓글 생성|POST|/api/articles/comments/|user|
|19|댓글 상세|GET|/api/articles/<int:comment_pk>/|all|
|20|댓글 수정|PUT|/api/articles/<int:comment_pk>/|user|
|21|댓글 삭제|DELETE|/api/articles/<int:comment_pk>/|user|
|22|게시글 좋아요|POST|/api/articles/<int:article_pk>/like/|user|
|23|게시글 좋아요 취소|DELETE|/api/articles/<int:article_pk>/like/|user|
|24|댓글 좋아요|POST|/api/articles/<int:comment_pk>/like/|user|
|25|댓글 좋아요 취소|DELETE|/api/articles/<int:comment_pk>/like/|user|
|26|인기글 목록|GET|/api/articles/popular/|all|
|27|예전글 목록|GET|/api/articles/past/|all|
|28|글 검색|GET|/api/articles/search/|all|
|29|News 목록|GET|/api/articles/nozonews/|all|
|30|ASK 목록|GET|/api/articles/ask/|all|
|31|Show 목록|GET|/api/articles/show/|all|
|32|카테고리 목록|GET|/api/articles/category/|all|
|33|크롤링 기사 목록|GET|/api/articles/news/|all|
|34|크롤링 기사 상세|GET|/api/articles/news/<int:pk>/|all|

------

## Wireframe

![Wireframe](https://github.com/user-attachments/assets/700d5306-2745-4eb6-b1ae-4bc477ec81e4)

------

## ERD

![ERD](https://github.com/user-attachments/assets/dfcde3fa-7be7-4c8e-8f6d-bea71f799900)
