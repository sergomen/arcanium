from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey('id_auth.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True, related_name='replies', on_delete=models.DO_NOTHING)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '{} by {} at {}'.format(self.text, self.author, self.created_date)