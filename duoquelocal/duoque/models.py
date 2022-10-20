from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Post(models.Model):
    clip = models.ImageField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')