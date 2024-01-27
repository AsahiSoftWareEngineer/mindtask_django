from django.urls import path, include
from . import views
from rest_framework import routers
app_name= 'api' 


urlpatterns = [
    path("task/", views.TaskView.as_view(), name="task"),
    path("task/delete/", views.TaskDeleteView.as_view(), name="task"),
    path("task/check/", views.TaskSwitchView.as_view(), name="task"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("token/set/", views.SetTokenService.as_view(), name="token_set"),
    path("refresh_token/get/", views.GetRefreshTokenService.as_view(), name="token_get"),
    path("has_refresh_token/", views.HasRefreshToken.as_view(), name="has_refresh_token"),
    path("is_expired_token/", views.IsExpireToken.as_view(), name="is_expire_token")
]

