from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User_Model(AbstractUser):
    reset_pass_code=models.CharField(max_length=76,null=True,blank=True)
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    activation_code=models.CharField(max_length=100,null=True,blank=True,verbose_name='activation code')
