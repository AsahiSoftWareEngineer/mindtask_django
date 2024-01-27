from django.contrib import admin
from .models import TaskModel, TodoModel
admin.site.register(TaskModel)
admin.site.register(TodoModel)
# Register your models here.
