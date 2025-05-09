from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Create your models here.

# class Record(models.Model):
#     create_at = models.DateTimeField(auto_now_add = True) #create_at = model.DateTimeField(auto_now_add = True)
#     first_name = models.CharField()
#     last_name = models.CharField()
#     email = models.EmailField()
#     phone = models.CharField()
#     is_admin = models.BooleanField(default=False)

# class Task(models.Model):
#     name = models.CharField(max_length=255)
#     due_date = models.DateTimeField(null=True, blank=True)
#     description = models.TextField(blank=True)
#     status = models.BooleanField(default=False)
#     people_involved = models.ForeignKey(Record,on_delete=models.CASCADE, related_name='tasks')


class Task(models.Model):
    STATUS_CHOICES = (
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')

    def __str__(self):
        return self.name
