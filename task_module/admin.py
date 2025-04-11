from django.contrib import admin

# Register your models here.
from .models import Task,Sub_Task,General_Task
admin.site.register(Task)
admin.site.register(Sub_Task)

