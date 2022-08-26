from rest_framework import serializers
from .models import Post, PostComment, PostLike, PostShare
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ("__all__")

class GETPostSerializer(serializers.ModelSerializer):
    select_related_fields = ('user','likes',)
    user = UserSerializer(many=False)
    likes = PostLikeSerializer(many=True)

    class Meta:
        model = Post
        fields = ("__all__")

class POSTPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("__all__")

class GETPostCommentSerializer(serializers.ModelSerializer):
    select_related_fields = ('user',)
    user = UserSerializer(many=False)

    class Meta:
        model = PostComment
        fields = ("__all__")

class POSTPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ("__all__")

class PostAndCommentsSerializer(serializers.ModelSerializer):
    select_related_fields = ('user','likes','comments')
    user = UserSerializer(many=False)
    likes = PostLikeSerializer(many=True)
    comments = GETPostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ("__all__")

class PostShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostShare
        fields = ["id", "body", "timestamp", "updated", "user", "post"]
