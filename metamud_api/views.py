from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from yaml import serialize
from .models import Post, PostComment, PostLike, PostShare
from .serializers import GETPostCommentSerializer, GETPostSerializer, POSTPostCommentSerializer, POSTPostSerializer, PostAndCommentsSerializer, PostLikeSerializer, PostShareSerializer
from django.contrib.auth.models import User

class PostListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        posts = Post.objects.select_related().all().order_by('-id')[:20]

        serializer = GETPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'body': request.data.get('body'), 
            'user': request.user.id
        }
        serializer = POSTPostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SinglePostListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        posts = Post.objects.select_related().filter(id=kwargs["id"])

        serializer = PostAndCommentsSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostShareListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        post_shares = PostShare.objects.all()
        serializer = PostShareSerializer(post_shares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'body': request.data.get('body'),
            'post': request.data.get('post'),
            'user': request.user.id
        }
        serializer = PostShareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostLikeListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        post_shares = PostLike.objects.all()
        serializer = PostLikeSerializer(post_shares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'post': request.data.get('post'),
            'user': request.user.id
        }
        serializer = PostLikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCommentListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        post_comments = PostComment.objects.filter(id=kwargs["id"])
        serializer = GETPostCommentSerializer(post_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'comment': request.data.get('comment'),
            'post': request.data.get('post'),
            'user': request.user.id
        }

        print("saw data", data)

        serializer = POSTPostCommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
