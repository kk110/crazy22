from django.contrib import admin
from web import models
from web import costom_user_admin

# Register your models here.
admin.site.register(models.Host)
# admin.site.register(models.UserProfile)   原先加密明文显示
admin.site.register(models.RemoteUser)
admin.site.register(models.HostGroups)
admin.site.register(models.BindHost)
admin.site.register(models.IDC)