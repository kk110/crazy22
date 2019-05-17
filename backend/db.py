import os
import getpass
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
            pwd = getpass.getpass("请输入密码:")  # getpass输入密码时不显示明文
            user = authenticate(username=username, password=pwd)
            if user is not None:
                print(("welcome,%s" % user).center(30, '-'))
                self.user = user
                return True
            else:
                retry_count += 1
                print('用户名或密码错误!')
        else:
            exit("--已到重试上限次数--")

    def interactive(self):
        # print("数据库交互部分")
        # 显示该账号绑定的组和未进组的主机
        exit_flag = False
        host_groups_list = self.user.host_groups.select_related()
        while True:
            # 显示未分组的主机列表   和    绑定主机组中的所有主机
            try:
                for i, group in enumerate(host_groups_list):
                    print('--%s  %s用户绑定的主机组共%s个，当前为%s--' % (
                    i, self.user, self.user.host_groups.select_related().count(), group))
                    print('--关联的未分组的主机列表:', self.user.bind_hosts.select_related())

                    user_choice = input("请选择主机组序号：")
                    if int(user_choice) < 0:
                        print("请输入正确主机组序号！！！")
                        continue
                    else:
                        print('--%s组中的所有主机：' % host_groups_list[i], group.bind_hosts.select_related())
            except Exception as e:
                print("出现错误啦！", e)
