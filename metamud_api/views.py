from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from yaml import serialize
from .models import Post, PostComment, PostLike, PostShare, CommentLike, HashtagFollow, Character
from .serializers import RegisterSerializer, CommentLikeSerializer, CharacterSerializer, HashtagFollowSerializer, GETPostCommentSerializer, GETPostSerializer, POSTPostCommentSerializer, POSTPostSerializer, PostAndCommentsSerializer, PostLikeSerializer, PostShareSerializer
from django.contrib.auth.models import User
from rest_framework import generics
import random

def charfilterl(s):
    return "".join([c for c in s if c.isalnum() or c == '-']).lower()

def charfilter(s):
    return "".join([c for c in s if c.isalnum() or c == '-'])

class RegisterListApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class PostListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        posts = None

        if 'hashtag' in kwargs:
            posts = Post.objects.select_related().filter(hashtag=kwargs['hashtag'])
            print("Hashtag in kwards")
        else:
            posts = Post.objects.select_related().all()
            print("Hashtag NOT in kwards")

        posts = posts.order_by('-id')[:20]

        serializer = GETPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 1. List all
    def post(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        posts = None

        hashtags = request.data.get('hashtags')

        if hashtags:
            posts = Post.objects.select_related().filter(hashtag__in=hashtags)
            print("Hashtag in kwards")
        else:
            posts = Post.objects.select_related().all()
            print("Hashtag NOT in kwards")

        posts = posts.order_by('-id')[:20]

        serializer = GETPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SinglePostListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        posts = Post.objects.select_related().filter(id=kwargs["pk"])

        serializer = PostAndCommentsSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'body': request.data.get('body').strip(), 
            'hashtag': request.data.get('hashtag').strip(),
            'user': request.user.id
        }

        data['hashtag'] = charfilterl(data['hashtag'])

        serializer = POSTPostSerializer(data=data)

        if serializer.is_valid() and data['body'] and data['hashtag']:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 2. Create
    def patch(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'key': charfilterl(request.data.get('key')),
            'value': request.data.get('value').strip(),
            'user': request.user.id
        }

        serializer = None

        if data['key'] in ['location']:
            instance = Post.objects.get(id=kwargs["pk"])

            if instance.user.id == request.user.id:
                new_data = {}
                new_data[data['key']] = data['value']

                serializer = POSTPostSerializer(instance=instance,
                                                data=new_data, # or request.data
                                                context={'author': request.user},
                                                partial=True)
                
                print("Serialized", serializer)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)
        else:
            print("Key not found", data['key'])

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EncounterListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'body': request.data.get('body').strip(),
            'hashtag': request.data.get('hashtag').strip(),
            'user': request.user.id
        }

        data['hashtag'] = charfilterl(data['hashtag'])

        serializer = POSTPostSerializer(data=data)

        data['action'] = "Battle"
        data['action_name'] = charfilter(request.data.get('action_name').strip())
        data['action_type'] = charfilterl(request.data.get('action_type').strip())
        data['action_level'] = int(request.data.get('action_level'))

        if data['action_level'] > 10: data['action_level'] = 10
        if data['action_level'] < 1: data['action_level'] = 1

        data['action_health'] = random.randint(data['action_level']*10, data['action_level']*100)
        data['action_weapon'] = "Sword"
        data['action_damage'] = "1 6"
        action_damage = data['action_damage'].split(" ")

        data['body'] = "A new challenger approaches! The {} {} (level {}) with {} health has entered the field. They carry a {} and deals {} d{}.\r\n\r\n{}".format(
            data['action_type'], data['action_name'], data['action_level'], data['action_health'],
            data['action_weapon'], action_damage[0], action_damage[1],
            data['body']
        )

        if serializer.is_valid() and data['body'] and data['hashtag']:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            'body': request.data.get('body').strip(),
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
        pass

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'post': request.data.get('post'),
            'user': request.user.id
        }

        existing_post = PostLike.objects.filter(user=data['user']).filter(post=data['post'])

        serializer = PostLikeSerializer(data=data)

        if serializer.is_valid() and not existing_post:
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
            'comment': request.data.get('comment').strip(),
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

    # 2. Create
    def patch(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'key': charfilterl(request.data.get('key')),
            'value': request.data.get('value').strip(),
            'user': request.user.id
        }

        serializer = None

        if data['key'] in ['location']:
            instance = PostComment.objects.get(id=kwargs["pk"])
            
            if instance.user.id == request.user.id:
                new_data = {}
                new_data[data['key']] = data['value']

                serializer = POSTPostCommentSerializer(instance=instance,
                                                data=new_data, # or request.data
                                                context={'author': request.user},
                                                partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentRollListApiView(APIView):
    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'comment': "",
            'post': request.data.get('post'),
            'user': request.user.id
        }

        dice_count = int(request.data.get('dice_count'))
        dice_size = int(request.data.get('dice_size'))

        if dice_count > 10: dice_count = 10
        if dice_size > 100: dice_size = 100

        rolls = [
            random.randint(1, dice_size)
            for i in range(dice_count)
        ]

        if dice_count > 0 and dice_size > 1:
            data["comment"] = "Rolled a {} ({}) with a D{}.".format(", ".join(
                [str(r) for r in rolls]), sum(rolls), dice_size)
            data["action"] = "Rolled"

            serializer = POSTPostCommentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentAttackListApiView(APIView):
    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'comment': "",
            'post': request.data.get('post'),
            'user': request.user.id
        }

        dice_count = 1
        dice_size = 6

        if dice_count > 10: dice_count = 10
        if dice_size > 100: dice_size = 100

        rolls = [
            random.randint(1, dice_size)
            for i in range(dice_count)
        ]

        post = Post.objects.get(id=data['post'])
        damage_dealt = sum(rolls)

        if post and dice_count > 0 and dice_size > 1:
            takes_damage = post.action_health > 0
            post.action_health = post.action_health-damage_dealt

            comment = request.data.get('comment').strip()
            health_remaining = "\r\n\r\n{} has {} health left!".format(post.action_name, post.action_health)

            if comment:
                comment = "\r\n\r\n{}".format(comment)
            
            if not takes_damage:
                health_remaining = ""
            elif takes_damage and post.action_health <= 0:
                health_remaining = "\r\n\r\n{} has been defeated!".format(post.action_name)

            data["comment"] = "[Attacked for {} ({}) with a D{}]{}{}".format(", ".join(
                [str(r) for r in rolls]), damage_dealt, dice_size, comment, health_remaining
                )
            data["action"] = "Attacked"

            serializer = POSTPostCommentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                post.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentLikeListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        pass

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'comment': request.data.get('comment'),
            'user': request.user.id
        }

        existing_post = CommentLike.objects.filter(user=data['user']).filter(comment=data['comment'])

        serializer = CommentLikeSerializer(data=data)

        if serializer.is_valid() and not existing_post:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HashtagFollowListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        following = HashtagFollow.objects.filter(user=request.user.id)
        serializer = HashtagFollowSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'hashtag': charfilterl(request.data.get('hashtag')),
            'user': request.user.id
        }

        existing_follow = HashtagFollow.objects.filter(user=data['user']).filter(hashtag=data['hashtag'])

        serializer = HashtagFollowSerializer(data=data)

        if serializer.is_valid() and not existing_follow:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
