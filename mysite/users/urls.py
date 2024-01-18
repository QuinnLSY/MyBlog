"""用户关联的url:https://127.0.0.1:8000/users/"""
from django.urls import path
from . import views

app_name = 'users'  # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('login.html', views.login_view, name='login'),
    path('register.html', views.register_view, name='register')
]
