from django.contrib import admin
from django.db import models
from .models import Task,Team,Comment
# Register your models here.
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Comment)

