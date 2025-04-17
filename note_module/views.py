from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import User_Note
from .forms import Note_Form
# Create your views here.

class Show_My_Notes(ListView):

    template_name = 'My_Notes.html'
    model=User_Note
    context_object_name = 'notes'
    paginate_by = 25
    def get_queryset(self):
        query=super().get_queryset().filter(creator_id=self.request.user)
        return query

    @login_required
    def get(self,*args,**kwargs):
        return super().get(*args,**kwargs)

class Create_Notes(View):
    def get(self,request):
        frm=Note_Form()
        return render(request,'Create_Note.html',context={'note_form':frm},status=200)
    
