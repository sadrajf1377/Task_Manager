
from rest_framework import serializers
from .models import Task,Sub_Task
class Task_Search_Serializer(serializers.ModelSerializer):
    completion_percentage=serializers.FloatField(read_only=Task,min_value=0,max_value=100)
    class Meta:
        model=Task
        fields=['title','deadline','completion_percentage']

class Subtask_Update_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Sub_Task
        fields=['title','description','is_done']
