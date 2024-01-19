""" 邮箱验证码发送 """

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string


def random_str(randomlength=8):
    """ 生成8位数的随机字符串方法"""
    chars = string.ascii_letters + string.digits  # 生成a-zA-z0-9字符串
    strcode = ''.join(random.sample(chars, randomlength))
    return strcode


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '博客注册激活链接'
        email_body = '请点击以下链接激活账号：http://127.0.0.1:8000/users/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, '13505508106@163.com', [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '博客找回密码链接'
        email_body = '请点击以下链接重设密码：http://127.0.0.1:8000/users/modify_pwd/{0}'.format(code)

        send_status = send_mail(email_title, email_body, '13505508106@163.com', [email])
        if send_status:
            pass
