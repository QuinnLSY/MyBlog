"""用户关联的url:https://127.0.0.1:8000/users/"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users'  # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('active/<active_code>', views.active_user, name='active'),
    path('forget_pwd/', views.forget_pwd, name='forget'),
    path('modify_pwd/<active_code>', views.modify_pwd, name='modify'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('editor_users/', views.editor_users, name='editor_users'),  # 编辑用户信息

]
