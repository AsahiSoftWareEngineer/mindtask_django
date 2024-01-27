from django.shortcuts import render
from django.views.generic import View;
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response

import json
# Create your views here.

from rest_framework import viewsets, filters

from .models import TaskModel, TodoModel
from .serializer import TaskSerializer, TodoSerializer
from .modules.auth import Account
from .modules.task import TaskManager
from .modules.profile import ProfileManager

def SetCookieResponse(params, cookies):
    res = HttpResponse(json.dumps(params))
    for i in cookies:
        res.set_cookie(key=i["key"], value=i["value"], httponly=True, max_age=i["max_age"])
    return res

def DeleteCookieResponse(params, cookies):
    res = HttpResponse(json.dumps(params))
    for i in cookies:
        res.delete_cookie(key=i["key"])
    return res

@method_decorator(csrf_exempt, name="dispatch")
class SetTokenService(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        return SetCookieResponse(
            {"response": 200},
            [
                {"key": "access_token", "value": params["accessToken"], "max_age": None},
                {"key": "refresh_token", "value": params["refreshToken"], "max_age": 60*60*24*30}
            ])

@method_decorator(csrf_exempt, name="dispatch")
class DeleteTokenService(View):
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        return DeleteCookieResponse(
            {"response": 200},
            [
                {"key": "access_token"},
                {"key": "refresh_token"}
            ]
        )
        
@method_decorator(csrf_exempt, name="dispatch")
class GetRefreshTokenService(View):
    def post(self, request, *args, **kwargs):
        refreshToken = request.COOKIES.get("refresh_token")
        return JsonResponse({"token": refreshToken})

@method_decorator(csrf_exempt, name="dispatch")
class HasRefreshToken(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({"response": request.COOKIES.get("refresh_token") != None})

@method_decorator(csrf_exempt, name="dispatch")
class IsExpireToken(View):
    def post(self, request, *args, **kwargs):
        try:
            Account().getUserId(request.COOKIES.get("access_token"))
            return JsonResponse({"response": False})
        except:
            return JsonResponse({"response": True})


    
class TaskView(APIView):
    def get(self, request, format=None):  
        token = request.COOKIES.get('access_token')
        user_id = Account().getUserId(token)
        manager = TaskManager(user_id, None)
        todayTask = manager.getTodayTask()
        nextdayTask = manager.getNextdayTask()
        return Response({
            "today": todayTask,
            "nextday": nextdayTask
        })
    
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        user_id = Account().getUserId(token)
        params = request.data
        manager = TaskManager(user_id, task_id=params["task_id"])
        task = manager.createNewTask()
        manager.insertNewTodoItem(todo_name=params["name"], uuid=params["uuid"])
        return Response({"id": task.id})


class TaskDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        user_id = Account().getUserId(token)
        params = request.data
        manager = TaskManager(user_id, task_id=params["task_id"])
        manager.deleteTask(params["uuid"])
        return Response({"response": 200})

class TaskSwitchView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        user_id = Account().getUserId(token)
        params = request.data
        manager = TaskManager(user_id, task_id=params["task_id"])
        manager.switchChecked(params["id"])
        return Response({"response": 200})


class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        user_id = Account().getUserId(token)
        manager = ProfileManager(user_id)
        return Response({
            "profile": manager.getProfile(),
            "continuation": manager.getContinution(),
            "stairs": manager.getStairs()
        })