from django.core.exceptions import ValidationError
from django.db import models

from user_module.models import User_Model
from datetime import datetime
from django.core.cache import cache

# Create your models here.
class General_Task(models.Model):
    description = models.TextField(verbose_name='main description of this task')
    title = models.CharField(max_length=200, verbose_name='title of this task')
    deadline = models.DateTimeField(null=False, blank=False)

    class Meta:
        abstract=True


class Task(General_Task):
    creator=models.ForeignKey(User_Model,on_delete=models.CASCADE,null=False,blank=False,db_index=True,related_name='tasks')
    creation_date=models.DateField(auto_now_add=True)
    last_modification_date = models.DateTimeField(verbose_name='when was the last time this task got modified',null=True,blank=True)
    def save(self,*args):
        self.last_modification_date=datetime.now()
        super().save(*args)


class Sub_Task(General_Task):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,null=False,blank=False,db_index=True,related_name='sub_tasks')
    is_done=models.BooleanField(default=False,verbose_name='is this subtask complete')
    def save(self,*args):
        if self.deadline>self.task.deadline:
            raise ValidationError("the subtask's deadline cannot be less than the parent task's deadline")
        self.task.last_modification_date=datetime.today()
        self.task.save()
        super().save(*args)
    def __str__(self):
        return f'this sub task belongs to the {self.task.title} task'





