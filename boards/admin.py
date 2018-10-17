from django.contrib import admin
from .models import Board, topic, post
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Board)
admin.site.register(topic)
admin.site.register(post)

