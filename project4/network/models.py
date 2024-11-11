from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True,unique = True)
    email = models.EmailField(primary_key = True)
    followers = models.ManyToManyField('self',symmetrical=False,related_name = 'following')

    def __str__(self):
        return self.username

class Post(models.Model):
    content = models.TextField(max_length = 500, blank=True)
    time = models.DateTimeField(auto_now_add = True)
    liked_by = models.ManyToManyField(User,related_name = "liked")
    posted_by = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "posts")

    def __str__(self):
        return f"\"{self.content[:30]}\" by {self.posted_by.username} - {self.time} id:{self.id}"

