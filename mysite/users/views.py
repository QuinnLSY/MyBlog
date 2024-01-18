""" 页面操作后显示内容 """
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.


""" 登录功能 """


def login_view(request):
    if request.method != 'POST':  # 不是post请求，显示空表单
        form = LoginForm()
    else:
        form = LoginForm(request.POST)  # 否则获取表单数据，进行登录验证
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print(username, password)
            # 与数据库中的用户名/密码比对，django默认保存密码是哈希形式存储，并不是明文，验证密码时调用User类的check_password方法，以哈希值比对
            user = authenticate(request, username=username, password=password)
            # 用户不为空
            if user is not None:
                login(request, user)  # 比对成功，进行登录
                return redirect('/admin')
            else:
                return HttpResponse('登录失败！请检查账号或密码！')

    context = {'form': form}
    return render(request, 'users/login.html', context)


""" 注册功能 """


def register_view(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)  # 否则获取表单数据，进行登录验证
        if form.is_valid():
            new_user = form.save(commit=False)  # 暂存验证过的数据，生成数据对象
            new_user.set_password(form.cleaned_data.get('password'))  # 将密码转换位哈希值存储
            new_user.username = form.cleaned_data.get('email')  # 将邮箱赋值给username
            new_user.save()
            return HttpResponse('注册成功！')

    context = {'form': form}
    return render(request, 'users/register.html', context)


""" 邮箱注册身份验证，在users/models.py中定义邮箱验证模型 """


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None
