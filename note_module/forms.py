from django import forms
from .models import User_Note

class Note_Form(forms.ModelForm):
    class Meta:
        model=User_Note
        fields=['title','note_importance','attached_file','content']
        labels={'title':"note's title",'attached_file':'attached file of this note (optional)','note_importance':'how important is this note','content':'main text of the note'}
        widgets={'title':forms.TextInput(attrs={'placeholder':'enter the tile of your note here'}),'attached_file':forms.FileInput(),'content':forms.Textarea()}


