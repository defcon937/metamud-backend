from django.urls import path
from .views import (
    PostCommentListApiView,
    PostLikeListApiView,
    PostListApiView,
    PostShareListApiView,
    SinglePostListApiView,
    CommentLikeListApiView,
    RegisterListApiView,
    CommentRollListApiView,
    EncounterListApiView,
    HashtagFollowListApiView,
    CommentAttackListApiView,
)

urlpatterns = [
    path('posts', PostListApiView.as_view()),
    path('posts/<str:hashtag>', PostListApiView.as_view()),
    path('post', SinglePostListApiView.as_view()),
    path('post/<int:pk>', SinglePostListApiView.as_view()),
    path('postshare', PostShareListApiView.as_view()),
    path('postlike', PostLikeListApiView.as_view()),
    path('commentlike', CommentLikeListApiView.as_view()),
    path('postcomment', PostCommentListApiView.as_view()),
    path('comment/<int:pk>', PostCommentListApiView.as_view()),
    path('encounter', EncounterListApiView.as_view()),
    path('simpleattack', CommentAttackListApiView.as_view()),
    path('postcommentroll', CommentRollListApiView.as_view()),
    path('register', RegisterListApiView.as_view(), name='auth_register'),
    path('follow', HashtagFollowListApiView.as_view()),
    path('character', RegisterListApiView.as_view()),
]
