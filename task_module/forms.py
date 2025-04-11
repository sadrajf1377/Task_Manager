from django import forms
from .models import Task,Sub_Task

class Create_Task_Form(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','deadline','description']
        labels={'title':'title of your task','deadline':'set the deadline date here','description':'describe your task here'}
        widgets={'title':forms.TextInput(),'deadline':forms.DateInput(),'description':forms.Textarea(attrs={'style':'resize:none'})}

class Create_Subtask_Form(forms.ModelForm):
    class Meta:
        model=Sub_Task
        fields=['title','task','description','deadline']
        labels={'title':'title of this sub task','description':'describe the subtask here','deadline':'last deadline of sub task'}
        widgets={'description':forms.Textarea(attrs={'style':'resize:none;outline:none'}),'task':forms.HiddenInput(attrs={'readonly':'true'})}


