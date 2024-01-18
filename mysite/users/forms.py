"""页面表单"""
from django import forms
from django.contrib.auth.models import User

"""登录页面表单，view.py中login_view调用"""


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))  # widget设置显示样式，PasswordInput自动显示密码为······

    # 自定义验证
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('用户名与密码不能相同！')
        return password


""" 注册页面表单，view.py中register_view调用"""


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='注册邮箱', max_length=32, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '请输入注册邮箱'
    }))
    password = forms.CharField(label='注册密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '请输入注册密码'
    }))  # widget设置显示样式，PasswordInput自动显示密码为······
    password1 = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '请确认密码'
    }))

    class Meta:
        model = User
        fields = ('email', 'password')

    # 自定义验证:邮箱
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已存在！')
        return email

    # 自定义验证：密码
    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']

        if password != password1:
            raise forms.ValidationError('两次输入的密码不一致，请修改！')
        return password1
