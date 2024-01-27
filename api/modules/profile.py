from accounts.models import User
from ..models import TaskModel, TodoModel, ProfileModel
from datetime import datetime, timedelta, timezone


class ProfileManager:
    def __init__(self, user_id):
        self.user = User.objects.get(id=user_id)
    
    
    def getProfile(self):
        return {
            "name": self.user.username,
        }
        
    def getContinution(self):
        task_count = TaskModel.objects.filter(user=self.user).count()
        return task_count -1 if (task_count > 0) else 0
        pass
    
    def getStairs(self):
        task_count = TodoModel.objects.filter(task__user=self.user, is_checked=True).count()
        return task_count
