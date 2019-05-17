import os
from web.models import Host
from django.contrib.auth import authenticate

class Interaction(object):
    def __init__(self, *args, **kwargs):
        # res = Host.objects.all()
        if self.authenticatie():
            self.interactive()

    def authenticatie(self):
        """用户认证"""
        retry_count = 0
        while retry_count < 3:
            username = input("请输入用户名:").strip()
            if len(username) == 0:
                print("用户名不能为空!")
                continue
            pwd = input("请输入密码:").strip()
            user = authenticate(username=username,password=pwd)
            if user is not None:
                print("welcome,%s"%user.center(30, '-'))
                self.user = user
                return True
            else:
                retry_count += 1
                print('用户名或密码错误!')
        else:
            exit("--已到重试上限次数--")

    def interactive(self):
        print("数据库交互部分")
