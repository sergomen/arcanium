from django.urls import path
from . import views

urlpatterns = [
    path('news', views.post_list, name='post_list'),
    path('news/post/<int:pk>/', views.news_post_detail, name='news_post_detail'),
    path('news/post/new/', views.news_post_new, name='news_post_new'),
    path('news/post/<int:pk>/edit/', views.news_post_edit, name='news_post_edit'),
    path('news/post/<int:pk>/comment/', views.news_add_comment_to_post, name='news_add_comment_to_post'),
    path('news_drafts/', views.news_post_draft_list, name='news_post_draft_list'),
    path('news_post/<pk>/publish/', views.news_post_publish, name='news_post_publish'),
    path('news_post/<pk>/remove/', views.news_post_remove, name='news_post_remove'),
    path('news_comment/<int:pk>/remove/', views.news_comment_remove, name='news_comment_remove'),
    path('news_post/<pk>/add_reply_to_comment', views.news_add_reply_to_comment, name='news_add_reply_to_comment'),
]