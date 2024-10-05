# todo_app/views.py
from django.shortcuts import render, redirect
from .models import User, Project, Todo
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Simple hash function for passwords
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hash_password(password)

        if not User.objects.filter(username=username).exists():
            User.objects.create(username=username, password=hashed_password)
            return redirect('login')
        else:
            return HttpResponse('User already exists.')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hash_password(password)

        user = User.objects.filter(username=username, password=hashed_password).first()

        if user:
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            return HttpResponse('Invalid credentials')

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def home(request):
    if 'user_id' not in request.session:
        return redirect('login')

    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})

def create_project(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        Project.objects.create(title=title)
        return redirect('home')

    return render(request, 'create_project.html')

def view_project(request, project_id):
    if 'user_id' not in request.session:
        return redirect('login')

    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        description = request.POST.get('description')
        Todo.objects.create(description=description, project=project)
        return redirect('view_project', project_id=project_id)

    todos = project.todos.all()
    return render(request, 'view_project.html', {'project': project, 'todos': todos})

def update_todo_status(request, todo_id):
    if 'user_id' not in request.session:
        return redirect('login')

    todo = get_object_or_404(Todo, id=todo_id)
    todo.status = not todo.status
    todo.save()
    return redirect('view_project', project_id=todo.project.id)

def delete_todo(request, todo_id):
    if 'user_id' not in request.session:
        return redirect('login')

    todo = get_object_or_404(Todo, id=todo_id)
    project_id = todo.project.id
    todo.delete()
    return redirect('view_project', project_id=project_id)

