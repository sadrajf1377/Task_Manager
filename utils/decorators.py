from django.http import HttpRequest
from rest_framework.response import Response

from Task_Manager.settings import API_KEY
def check_api_key(func):
    def wrapper(*args,**kwargs):
        request:HttpRequest=args[0] or kwargs['request']
        if request.headers.__contains__('api_key') and request.headers.get('api_key')==API_KEY:
            return func(*args,**kwargs)
        else:
            return Response(data={'message':'the given api key was not correct'},status=401)
    return wrapper


