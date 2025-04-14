
from django.urls import path
from .views import Login_Singup_Page,Login,Logout,Signup
# Create your tests here.
urlpatterns=[
    path('login_signup/<to_render>',Login_Singup_Page.as_view(),name='load_login_signup'),
    path('login',Login.as_view(),name='login_user'),
    path('signup_user',Signup.as_view(),name='signup_user'),
    path('logout',Logout.as_view(),name='logout')
]