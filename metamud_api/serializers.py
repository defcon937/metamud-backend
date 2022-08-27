from rest_framework import serializers
from .models import Post, PostComment, PostLike, PostShare, CommentLike
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        if validated_data['first_name'] != 'test':
            return False
        
        final_username = "".join([c for c in validated_data['username'] if c.isalnum() or c == '-']).lower()

        if final_username != validated_data['username']:
            return False

        user = User.objects.create(
            username=final_username,
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ("__all__")

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
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
    likes = CommentLikeSerializer(many=True)

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
