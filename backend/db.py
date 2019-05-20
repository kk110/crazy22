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
        while not exit_flag:
            # 显示未分组的主机列表   和    绑定主机组中的所有主机
            try:
                for i, group in enumerate(host_groups_list):
                    print('[ %s >>>]' % self.user)
                    print('序号：%s   组名: %s' % (i, group))
                    # print('--%s  %s用户绑定的主机组共%s个，当前为%s--' % (
                    #     i, self.user, self.user.host_groups.select_related().count(), group) self.user.bind_hosts.select_related())
                    print('序号：z   未分组主机')

                user_choice = input("请选择主机组序号：")
                print("--用户输入-", user_choice)
                if user_choice.isdigit():
                    user_choice = int(user_choice)
                    if user_choice >= 0 and (user_choice < len(host_groups_list)):
                        print('--%s组中的所有主机：' % host_groups_list[user_choice])
                        # host_groups_list[user_choice].bind_hosts.select_related())
                        for j, host in enumerate(host_groups_list[user_choice].bind_hosts.select_related()):
                            print('序号: %s, 主机: %s' % (j, host))
                    else:
                        print("请输入正确的主机组序号！！！")
                else:
                    if user_choice == "z":
                        not_group_list = self.user.bind_hosts.select_related()
                        while not exit_flag:
                            for i, host_obj in enumerate(not_group_list):
                                print("----未分组主机列表----")
                                print("序号：%s, 未分组主机: %s" % (i, host_obj))

                            user_choice2 = input("请输入未分组主机序号(输入b返回上一级)：")
                            if user_choice2.isdigit():
                                user_choice2 = int(user_choice2)
                                if user_choice2 >= 0 and user_choice2 <= len(not_group_list):
                                    print('未分组主机： %s' % not_group_list[user_choice2])
                            elif user_choice2 == "b":
                                break
                    elif user_choice == "exit":
                        exit_flag = True
                        print("bye~")

            except Exception as e:
                if e == 'KeyboardInterrupt':
                    continue
                else:
                    print("出现错误啦！", e)
