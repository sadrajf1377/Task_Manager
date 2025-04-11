from django import forms
from user_module.models import User_Model
import re
password_pattern=r'(?=.*[A-Z].*)(?=.*[0-9].*)(?=[[!@#$%^&*.]])'
class Login_Form(forms.Form):
    username_email=forms.CharField(max_length=20,label='username_email',required=True,
                                   widget=forms.TextInput(attrs={'placeholder':'enter your email or username here'}))
    password=forms.CharField(max_length=25,required=True,label='password',widget=forms.PasswordInput())


class Signup_Form(forms.ModelForm):
    class Meta:
        model=User_Model
        fields=['username','email','password']
    password_repeat=forms.CharField(max_length=25,required=True,label='password_repeat',widget=forms.PasswordInput())
    def is_valid(self):
        is_valid=super().is_valid()
        valid_password=re.match(password_pattern,self.password)
        passwords_match=self.password==self.password_repeat
        if not valid_password:
            self.add_error('password_repeat','password must contain at least:one number,one uppercase character and one special character ex:@!')
        if not passwords_match:
            self.add_error('password_repeat','passwords do not match!')
        return is_valid and passwords_match and valid_password



