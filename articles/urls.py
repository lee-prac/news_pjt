from django.urls import path
from . import views

app_name="articles"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article"),
    path("category/", views.CategoryListView.as_view()),
    path("<int:pk>/", views.ArticleDetailView.as_view()),
    
    path('news/', views.NewsViewSet.as_view({'get': 'list'}), name='news_list'), 
    path('news/<int:pk>/', views.NewsViewSet.as_view({'get': 'retrieve'}), name='news_detail'), 

    path('comments/', views.CommentViewSet.as_view({'get': 'list'}), name='comment_list'), 
    path('comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve'}), name='comment_detail'), 
]
