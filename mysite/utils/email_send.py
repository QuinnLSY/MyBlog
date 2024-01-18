""" 邮箱验证码发送 """

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string
