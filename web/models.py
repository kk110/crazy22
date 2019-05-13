from django.db import models
# from django.contrib.auth.models import User
from web.auth import UserProfile

# Create your models here.
class IDC(models.Model):
    """机房"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    """主机信息"""
    host_name = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField()
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey('IDC', blank=True, null=True, on_delete=models.CASCADE)
    system_type_choices = ((0, 'linux'), (1, 'windows'))
    system_type = models.SmallIntegerField(choices=system_type_choices, default=0)
    memo = models.CharField(max_length=128, blank=True, null=True)  # 备注
    enabled = models.BooleanField(default=1, verbose_name='启用本机')  # 是否禁用主机

    def __str__(self):
        return "%s(%s)" % (self.host_name, self.ip_addr)

    class Meta:
        unique_together = ('ip_addr', 'port')  # 联合唯一


class RemoteUser(models.Model):
    """存储远程用户信息"""
    auth_type_choice = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choice, default=0)
    user_name = models.CharField(max_length=128)
    password = models.CharField(max_length=256, help_text='如果此处auth_type选择为ssh-key,那此处应该为key')  # 密码存密文\明文

    def __str__(self):
        return self.user_name

    class Meta:
        unique_together = ('auth_type', 'user_name', 'password')


# class UserProfile(models.Model):
#     """堡垒机账号"""
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     name = models.CharField(max_length=64)
#
#     def __str__(self):
#         return self.name


class BindHost(models.Model):
    """关联主机和远程用户信息"""
    host = models.ForeignKey('Host',on_delete=models.CASCADE)
    remote_user = models.ForeignKey('RemoteUser',on_delete=models.CASCADE)

    def __str__(self):
        return '<%s:%s>' % (self.host, self.remote_user)

    class Meta:
        unique_together = ('host', 'remote_user')


class HostGroups(models.Model):
    """主机组，所有属于这个主机组的用户可访问"""
    name = models.CharField(max_length=64, unique=True)
    bind_hosts = models.ManyToManyField('BindHost', blank=True)
    memo = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name
