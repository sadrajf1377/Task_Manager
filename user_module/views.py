from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from user_module.models import User_Model

# Create your views here.
class Index_Paage(View):
    def get(self,request):
        unfinished_tasks=None

class Update_User_Info(UpdateView):
    model = User_Model
    template_name = ''
    success_url = reverse_lazy()
    fields =['email','username','phone_number','first_name','last_name']
    def get_object(self, queryset=None):
        obj=self.request.user
        return obj
