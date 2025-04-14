
from django.urls import path
from .views import Login_Singup_Page,Login,Logout
# Create your tests here.
urlpatterns=[
    path('login_signup',Login_Singup_Page.as_view(),name='load_login_signup'),
    path('login',Login.as_view(),name='login_user'),
    path('logout',Logout.as_view(),name='logout')
]