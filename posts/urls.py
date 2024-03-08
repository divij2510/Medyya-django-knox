from django.urls import path
from posts import views  

app_name = 'posts_api'

urlpatterns = [
    # Post management endpoints
    path('create/', views.CreatePostAPIView.as_view(), name='create-post'),
    path('delete/<int:post_id>/', views.DeletePostAPIView.as_view(), name='delete-post'),
    path('view/all/', views.PostsListAPIView.as_view(), name='view-all-posts'),

    # Like/unlike management endpoints
    path('like/<int:post_id>/', views.LikePostAPIView.as_view(), name='like-post'),
    path('unlike/<int:post_id>/', views.UnlikePostAPIView.as_view(), name='unlike-post'),
]
