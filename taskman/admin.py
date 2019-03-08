from django.contrib import admin
from django.db import models
from .models import Task
# Register your models here.
admin.site.register(Task)