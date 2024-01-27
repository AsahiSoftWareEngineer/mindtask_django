# coding: utf-8

from rest_framework import serializers
from .models import TaskModel, TodoModel

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel()
        fields = ('name',)
    
    def create(self, validated_data):
        print(validated_data)
        pass
        
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        task = TodoSerializer()
        fields = ('created_at', 'updated_at')


