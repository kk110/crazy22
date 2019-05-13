# Generated by Django 2.2.1 on 2019-05-10 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BindHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_type', models.SmallIntegerField(choices=[(0, 'ssh-password'), (1, 'ssh-key')], default=0)),
                ('user_name', models.CharField(max_length=128)),
                ('password', models.CharField(help_text='如果此处auth_type选择为ssh-key,那此处应该为key', max_length=256)),
            ],
            options={
                'unique_together': {('auth_type', 'user_name', 'password')},
            },
        ),
        migrations.CreateModel(
            name='HostGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('memo', models.CharField(blank=True, max_length=128, null=True)),
                ('bind_hosts', models.ManyToManyField(blank=True, to='web.BindHost')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=64, unique=True)),
                ('ip_addr', models.GenericIPAddressField()),
                ('port', models.SmallIntegerField(default=22)),
                ('system_type', models.SmallIntegerField(choices=[(0, 'linux'), (1, 'windows')], default=0)),
                ('memo', models.CharField(blank=True, max_length=128, null=True)),
                ('enabled', models.BooleanField(default=1, verbose_name='启用本机')),
                ('idc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.IDC')),
            ],
            options={
                'unique_together': {('ip_addr', 'port')},
            },
        ),
        migrations.AddField(
            model_name='bindhost',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Host'),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='remote_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.RemoteUser'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhost',
            unique_together={('host', 'remote_user')},
        ),
    ]
