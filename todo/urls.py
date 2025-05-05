from django.urls import path
from django.contrib import admin
from todo import views as todo_views
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('task_list', views.task_list, name="task_list"),
    path('register/', todo_views.register, name='register'),
    path('login/', todo_views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('task/<int:task_id>/update/', todo_views.update_status, name='update_status'),
    # path('create/', todo_views.create_task, name='create_task'),
]