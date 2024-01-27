from django.db import models
from accounts.models import User
# Create your models here.

class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class TodoModel(models.Model):
    uuid = models.TextField()
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class ProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    
    