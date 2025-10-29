from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# 创建注册表单
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='邮箱')
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': '用户名',
            'password1': '密码',
            'password2': '确认密码',
        }

