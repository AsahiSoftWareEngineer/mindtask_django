from accounts.models import User
from ..models import TaskModel, TodoModel
from datetime import datetime, timedelta, timezone


JST = timezone(timedelta(hours=9), "JST")
class TaskManager:
    def __init__(self, user_id:int, task_id:int)->None:
        self.user = User.objects.get(id=user_id)
        self.task =  TaskModel.objects.get(id=task_id, user=self.user) if TaskModel.objects.filter(id=task_id, user=self.user).exists() else None
        
        
    def createNewTask(self)->object:
        now_datetime = datetime.now(JST)
        if(self.task is not None):
            return self.task
        else:
            self.task = TaskModel.objects.create(
                user=self.user,
                created_at=now_datetime,
                updated_at=now_datetime,
            )
            return self.task
        
    
    def insertNewTodoItem(self, todo_name:str, uuid:str)->object:
        now_datetime = datetime.now(JST)
        todo = TodoModel.objects.update_or_create(
            uuid=uuid,
            defaults={
                "task":self.task,
                "name":todo_name,
                "is_checked":False,
                "created_at":now_datetime,
                "updated_at":now_datetime
            }
        )
        return todo
    
    def getTodayTask(self):
        now_datetime = datetime.now(JST) + timedelta(days=-1)
        print(now_datetime)
        if(TaskModel.objects.filter(
            user=self.user,
            created_at__year=now_datetime.year,
            created_at__month=now_datetime.month,
            created_at__day=now_datetime.day).exists()
           ): 
            task = TaskModel.objects.get(
            user=self.user,
            created_at__year=now_datetime.year,
            created_at__month=now_datetime.month,
            created_at__day=now_datetime.day)
            
            todo = TodoModel.objects.filter(task=task)
            todo_array = [{"id": i.id, "name": i.name, "is_checked": i.is_checked} for i in todo]
            return {
                "tasks": todo_array,
                "id": task.id,
            }
        else:
            return {
                "tasks": [],
                "id": None
            }
    
    def getNextdayTask(self):
        now_datetime = datetime.now(JST)
        if(TaskModel.objects.filter(
            user=self.user,
            created_at__year=now_datetime.year,
            created_at__month=now_datetime.month,
            created_at__day=now_datetime.day,
        )):
            task = TaskModel.objects.get(
            user=self.user,
            created_at__year=now_datetime.year,
            created_at__month=now_datetime.month,
            created_at__day=now_datetime.day)
            
            todo = TodoModel.objects.filter(task=task)
            todo_array = [{"id": i.uuid, "name": i.name, "is_checked": i.is_checked} for i in todo]
            return {
                "tasks": todo_array,
                "id": task.id,
            }
        else:
            return {
                "tasks":[],
                "id": None,
            }
    
    def deleteTask(self, uuid):
        if(TodoModel.objects.filter(uuid=uuid, task=self.task)):
            TodoModel.objects.filter(task=self.task).delete()
        return None
    
    def switchChecked(self, id):
        if(TodoModel.objects.filter(id=id).exists()):
            task = TodoModel.objects.get(id=id)
            task.is_checked = not task.is_checked
            task.save()
        return None
        
    
        
        
        
    
    