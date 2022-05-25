from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<pk>/add_reply_to_comment', views.add_reply_to_comment, name='add_reply_to_comment'),
]