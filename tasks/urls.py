
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/completed/', tasks_completed, name='tasks_completed'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task_details, name='task_details'),
    path('tasks/<int:task_id>/complete', complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', delete_task, name='delete_task'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', signout,name='logout'),
    
]