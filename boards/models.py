from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
import math

class Board(models.Model):
    Name = models.CharField(max_length =30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.Name

    def get_posts_count(self):
        return post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return post.objects.filter(topic__board=self).order_by('-created_at').first()


class topic(models.Model):
    subject = models.CharField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    last_updated = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count/20
        return math.ceil(pages)

    def has_many_pages(self,count=None):
        if count == None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1,5)
        else:
            return range(1,count+1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]



class post(models.Model):
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='+')
    topic = models.ForeignKey(topic, on_delete=models.CASCADE, related_name='posts')


    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))




