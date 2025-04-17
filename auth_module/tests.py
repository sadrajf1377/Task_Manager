from django.test import TestCase
from django.urls import reverse

from user_module.models import User_Model
class Test_Login(TestCase):
    def setUp(self):
        user=User_Model(username='username',email='test@test.com')
        user.set_password('1234')
        user.save()
        self.login_with_incorrect_data_form=self.client.post(reverse('login_user'),data={'username_email':'username'}).status_code
        self.login_with_incorrect_creds=self.client.post(reverse('login_user'),data={'username_email':'username','password':'123456'}).status_code
        self.correct_login_view_status=self.client.post(reverse('login_user'),data={'username_email':'username','password':'1234'}).status_code

    def test(self):
        self.assertEqual(self.correct_login_view_status,302,msg='failed to login with correct creds')
        self.assertEqual(self.login_with_incorrect_creds, 404, msg='logged in with false creds')
        self.assertEqual(self.login_with_incorrect_data_form, 400, msg='logged in with improper data format')


class Test_Signup(TestCase):
    def setUp(self):
        data1={'username':'username','email':'test@test.com','password':'2455','password_repeat':'2455'}
        self.weak_password_signup=self.client.post(reverse('signup_user'),data=data1).status_code
        data2={'username':'username1','email':'email@email.com','password':'Test!12345','password_repeat':'Test!12345'}
        self.strong_password_signup=self.client.post(reverse('signup_user'),data=data2).status_code
        data3={'username':'username2','email':'email2@email.com','password':'Test_12345','password_repeat':'Test_3564'}
        self.not_matching_passwords_signup=self.client.post(reverse('signup_user'),data=data3).status_code

    def test(self):
        self.assertEqual(self.weak_password_signup,400,msg='signed up a user with weak password')
        self.assertEqual(self.strong_password_signup,201,msg='failed to create a user with correct creds and strong password')
        self.assertEqual(self.not_matching_passwords_signup,400,msg='signed up a user without having matched passwords')




