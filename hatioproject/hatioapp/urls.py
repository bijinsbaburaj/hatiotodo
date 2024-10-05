# todo_project/urls.py
from django.urls import path
from hatioapp import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.view_project, name='view_project'),
    path('todo/update_status/<int:todo_id>/', views.update_todo_status, name='update_todo_status'),
    path('todo/delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
