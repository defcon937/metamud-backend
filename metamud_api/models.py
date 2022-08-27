from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    body = models.TextField(max_length = 2048)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    hashtag = models.CharField(max_length=255, blank=True)
    action = models.CharField(blank = True, max_length=255)
    action_name = models.CharField(blank = True, max_length=255)
    action_type = models.CharField(blank = True, max_length=255)
    action_level = models.IntegerField(default=0)
    action_health = models.IntegerField(default=0)
    action_weapon = models.CharField(blank = True, max_length=255)
    action_damage = models.CharField(blank = True, max_length=255)
    location = models.CharField(blank = True, max_length=255)

    def __str__(self):
        return self.body

class PostShare(models.Model):
    body = models.TextField(max_length = 1024)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.body

class PostComment(models.Model):
    comment = models.TextField(max_length = 2048)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank = True, null = True, related_name="comments")
    action = models.CharField(blank = True, max_length=255)
    location = models.CharField(blank = True, max_length=255)

    def __str__(self):
        return self.comment

class PostLike(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank = True, null = True, related_name="likes")

    def __str__(self):
        return str(self.timestamp)

class CommentLike(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    comment = models.ForeignKey(PostComment, on_delete = models.CASCADE, blank = True, null = True, related_name="likes")

    def __str__(self):
        return str(self.timestamp)

class HashtagFollow(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    hashtag = models.CharField(max_length=255)

    def __str__(self):
        return str(self.hashtag)

class Character(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length = 2048)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    hashtag = models.CharField(max_length=255, blank=True)
    hero_type = models.CharField(max_length=100, blank=True)
    health = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    weapon = models.CharField(max_length=100, blank=True)
    weapon_damage = models.CharField(blank = True, max_length=255)
    
    def __str__(self):
        return self.name
