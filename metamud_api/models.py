from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    body = models.TextField(max_length = 2048)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    hashtag = models.CharField(max_length=255, blank=True)

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

    def __str__(self):
        return self.comment

class PostLike(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank = True, null = True, related_name="likes")

    def __str__(self):
        return self.body
