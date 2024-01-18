"""" 超级管理员设置：https://127.0.0.1:800/admin"""
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, EmailVerifyRecord
# Register your models here.
from django.contrib.auth.admin import UserAdmin  # 官方默认管理员注册

# 取消用户关联注册
admin.site.unregister(User)


# 定义关联对象样式，StackedInline位纵向排列，tabularInline位并排排列
class UserProfileInline(admin.StackedInline):
    model = UserProfile  # 关联的模型


# 关联UserProfile
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


# 注册User模型
admin.site.register(User, UserProfileAdmin)


# adminview调用邮箱验证码(在admin网页中可查看管理，utils/email_send.py中实现发送)
@admin.register(EmailVerifyRecord)
class Admin(admin.ModelAdmin):
    """Admin view for"""

    list_display = ('code',)
