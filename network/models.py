from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)
    likes = models.ManyToManyField('Post', blank=True, related_name="liked_users")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)





