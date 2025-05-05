from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task

class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.ChoiceField(
        choices=[(True, 'Admin'), (False, 'User')],
        widget=forms.RadioSelect,
        label='Role'
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff']


class TaskForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'status', 'assigned_users']