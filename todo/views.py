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
from django.shortcuts import get_object_or_404

User = get_user_model()

@login_required
def task_list(request):
    # tasks = request.user.tasks.all() #use when filtering for specific user, later feature
    tasks = Task.objects.all()

    form = None
    if request.user.is_staff:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save()
                assigned = request.POST.getlist('assigned_users')
                task.assigned_users.set(assigned)
                return redirect('task_list')
            else:
                form = TaskForm()
    
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'is_admin': request.user.is_staff, 'form': form})

@login_required
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    # if not request.user.is_staff and request.user not in task.assigned_users.all():
    #     return redirect('task_list')

    # if user is admin -> admin side
    if request.user.is_staff:
        if request.method == 'POST':
            if 'delete' in request.POST:
                task.delete()
                return redirect('task_list')
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
            return redirect('task_list')
        else:
            form = TaskForm(instance=task)
        return render(request, 'todo/edit_task.html', {'form': form, 'task': task})
    
    #user must be regular -> user side
    if request.method == 'POST':
        task.status = request.POST['status']
        task.save()
        return redirect('task_list')
        
    return render(request, 'todo/update_task.html', {'task': task})

# @login_required
# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)

#     if request.user.is_staff:
#         task.delete()
#         return redirect('task_list')