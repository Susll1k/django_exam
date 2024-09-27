from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CustomUser(AbstractUser):
    picture = models.ImageField(upload_to='profile_pics', verbose_name='Аватар', null=True, blank=True, default='default/sbcf-default-avatar.webp')

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null=True)
    title= models.CharField(max_length=255)
    image= models.ImageField(upload_to='posts')



class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='reviews_author')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Like(models.Model):
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='likes_author')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('author', 'post')

