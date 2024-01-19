""" 页面操作后显示内容 """
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import EmailVerifyRecord, UserProfile
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required

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
                return redirect('users:user_profile')
            else:
                return HttpResponse(
                    '登录失败！请检查账号或密码！<br> (三秒后自动跳转...) '
                    '<script>setTimeout(function() {window.location.href = "/users/login/";}, 3000);</script>'
                )

    context = {'form': form}  # 上下文
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

            # 发送邮件
            send_register_email(form.cleaned_data.get('email'), 'register')
            return HttpResponse(
                '注册成功！请前往邮箱验证！<br> (即将跳转到登录页面...) '
                '<script>setTimeout(function() {window.location.href = "/users/login/";}, 3000);</script>'
            )

    context = {'form': form}
    return render(request, 'users/register.html', context)


""" 邮箱注册身份验证，在users/models.py中定义邮箱验证模型 """


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, ):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None


""" 修改用户状态，邮箱链接点击后跳转页面"""


def active_user(request, active_code):
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('链接有误')
    return redirect('users:login')


""" 找回密码 """


def forget_pwd(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, 'forget')
                return HttpResponse('邮件已发送请查收！')
            else:
                return HttpResponse(
                    '邮箱还未注册，请前往注册！<br> (三秒后自动跳转...) '
                    '<script>setTimeout(function() {window.location.href = "/users/register/";}, 3000);</script>'
                )
    context = {'form': form}
    return render(request, 'users/forget_pwd.html', context)


""" 修改密码 """


def modify_pwd(request, active_code):
    if request.method == 'GET':
        form = ModifyPwdForm()
    elif request.method == 'POST':
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse(
                '密码修改成功，快去登录吧！<br> (三秒后自动跳转...) '
                '<script>setTimeout(function() {window.location.href = "/users/login/";}, 3000);</script>'
            )
        else:
            return HttpResponse('密码修改失败！快检查检查！')

    context = {'form': form}
    return render(request, 'users/modify_pwd.html', context)


""" 个人中心 """


@login_required(login_url='users:login')  # 设置登录后才能访问，如果没有登录就跳转到登录页面
def user_profile(request):
    user = User.objects.get(username=request.user)  # 获取当前用户
    return render(request, 'users/user_profile.html', {'user': user})


"""登出"""


def logout_view(request):
    logout(request)
    return redirect('users:login')


""" 编辑用户信息 """


@login_required(login_url='users:login')   # 登录之后允许访问
def editor_users(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()

                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    return render(request, 'users/editor_users.html', locals())
