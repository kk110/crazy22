from django.db import models


# from django.contrib.auth.models import User
# from web.auth import UserProfile

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

class SessionRecord(models.Model):
    """存储ssh登录的各种信息"""
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name='堡垒机账号')
    bind_host = models.ForeignKey("BindHost", on_delete=models.CASCADE, verbose_name='登录主机及远程账户')
    random_tag = models.CharField(max_length=64, verbose_name='随机标签')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s  %s' % (self.user.email, self.bind_host)


class BindHost(models.Model):
    """关联主机和远程用户信息"""
    host = models.ForeignKey('Host', on_delete=models.CASCADE)
    remote_user = models.ForeignKey('RemoteUser', on_delete=models.CASCADE)

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


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        '''email是唯一标识，没有会报错'''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)  # 检测密码合理性
        user.save(using=self._db)  # 保存密码
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(email,
                                password=password,
                                name=name
                                )
        user.is_admin = True  # 比创建用户多的一个字段
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    # 由于在单独文件中无法导入BindHost和HostGroup模块，所以将两文件集合到一起
    bind_hosts = models.ManyToManyField(BindHost, blank=True)
    host_groups = models.ManyToManyField(HostGroups, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()  # 创建用户

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    '''django自带后台权限控制，对哪些表有查看权限等'''

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    '''用户是否有权限看到app'''

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
