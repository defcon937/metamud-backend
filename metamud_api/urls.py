from django.urls import path
from .views import (
    PostCommentListApiView,
    PostLikeListApiView,
    PostListApiView,
    PostShareListApiView,
    SinglePostListApiView,
)

urlpatterns = [
    path('post', PostListApiView.as_view()),
    path('post/<int:id>', SinglePostListApiView.as_view()),
    path('postshare', PostShareListApiView.as_view()),
    path('postlike', PostLikeListApiView.as_view()),
    path('postcomment', PostCommentListApiView.as_view())
]
