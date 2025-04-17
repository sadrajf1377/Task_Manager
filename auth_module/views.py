from django.contrib.auth import logout, login
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import Login_Form,Signup_Form
from user_module.models import User_Model
from rest_framework.authtoken.models import Token
from utils.decorators import check_api_key
from Task_Manager.settings import SECRET_KEY
# Create your views here.
class Login_Singup_Page(View):
    def get(self,request,to_render):
        if to_render=='signup' or to_render=='login':
            frm=Signup_Form() if to_render=='signup' else Login_Form()
            return render(request, 'Login&Signup.html',
                          context={'form':frm,'type':to_render})
        else:
            return render(request,'404.html',status=404)



class Login(View):
    def post(self,request):
        frm=Login_Form(request.POST)
        if frm.is_valid():

            try:
                user_email=frm.cleaned_data.get('username_email')
                user=User_Model.objects.get(Q(email=user_email)|Q(username=user_email))

                if user.check_password(frm.cleaned_data.get('password')):
                    login(request=request,user=user)
                    return redirect(reverse('load_index'))
                else:
                    frm.add_error('password','user not found')
                    return render(request, 'Login&Signup.html',
                                  context={'form':frm,'type':'login'},status=404)
            except Exception as e:
                print(e)
                frm.add_error('password', 'user not found')
                return render(request, 'Login&Signup.html',
                              context={'form':frm,'type':'login'},status=404)
        else:
            return render(request,'Login&Signup.html',context={'form':frm,'type':'login'},status=400)


@method_decorator(check_api_key,name='dispatch')
class Login_Api(APIView):
    http_method_names = ['POST']
    def post(self,request):
        data=request.data
        username_email=data['username_email']
        password=data['password']
        try:
            user=User_Model.objects.get(Q(username=username_email)|Q(email=username_email))
            if user.check_password(password):
                tok=Token(user_id=user.id)
                tok.save()
                return Response(data={'message':f'your authentication was successful','token':str(tok.key)},status=201)
            else:
                return Response(data={'message':'user with such credentials was not found!'},status=404)
        except Exception as e:
            if isinstance(e,User_Model.DoesNotExist):
                return Response(data={'message': 'user with such credentials was not found!'}, status=404)
            else:
                return Response(data={'message': 'an unknown error happend!please try again'}, status=500)



class Signup(View):
    def post(self,request):
        frm=Signup_Form(request.POST)
        if frm.is_valid():
            try:
                with transaction.atomic():
                    act_code=get_random_string(length=72)
                    password=frm.cleaned_data.get('password')
                    frm.instance.set_password(password)
                    frm.instance.activation_code=act_code
                    frm.save()
                    return render(request,'Message.html',context={'message':f'User Was Created SuccessFully!credintials are password:{password},username:{frm.cleaned_data.get("username")}',},status=201)
            except Exception as e:

                frm.add_error('password','an error happend,please try again')
                return render(request,'Login&Signup.html',context={'form':frm,'type':'signup'},status=500)
        else:

            return render(request, 'Login&Signup.html', context={'form':frm,'type':'signup'},status=400)


class Logout(View):
    def get(self,request):
        logout(request=request)
        return redirect(reverse('load_index'))