from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import CustomUserCreationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)
            login(request, user)
            return redirect('task_list')
        else: 
            print("Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'todo/register.html', {'form': form})

def login(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'todo/login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'todo/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def task_list(request):
    # tasks = Task.objects.all()
    return render(request, 'todo/task_list.html')#, {'tasks': tasks})

# @login_required
# def update_status(request, task_id):
#     task = Task.objects.get(id=task_id)
#     if request.user in task.assigned_users.all():
#         if request.method == 'POST':
#             task.status = request.POST.get('status')
#             task.save()
#             return redirect('task_list')
#     return render(request, 'update_status.html', {'task': task})

# @login_required
# def create_task(request):
#     if request.user.user_type != 'admin':
#         return redirect('task_list')
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save()
#             assigned = request.POST.getlist('assigned_users')
#             task.assigned_users.set(assigned)
#             return redirect('task_list')
#     else:
#         form = TaskForm()
#     return render(request, 'create_task.html', {'form': form})