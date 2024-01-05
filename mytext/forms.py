from django import forms
from mytext import models
from mytext.models import Post

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(label='您的帳號', max_length=50)
    user_email = forms.EmailField(label='電子郵件')
    user_password = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    user_password_confirm = forms.CharField(label='確認密碼', widget=forms.PasswordInput) 
    
class LoginForm(forms.Form):
    user_name = forms.CharField(label='您的帳號', max_length=50)
    user_password = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)