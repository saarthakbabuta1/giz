# Generated by Django 4.0 on 2022-01-01 17:32

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=254, unique=True, verbose_name='Unique UserName')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('mobile', models.CharField(blank=True, max_length=150, null=True, unique=True, verbose_name='Mobile Number')),
                ('name', models.CharField(max_length=500, verbose_name='Full Name')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='Profile Photo')),
                ('is_active', models.BooleanField(default=False, verbose_name='Activated')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Status')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('token', models.TextField(verbose_name='JWT Access Token')),
                ('session', models.TextField(verbose_name='Session Passed')),
                ('refresh_token', models.TextField(blank=True, verbose_name='JWT Refresh Token')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='Expires At')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create Date/Time')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Date/Time Modified')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.user')),
            ],
            options={
                'verbose_name': 'Authentication Transaction',
                'verbose_name_plural': 'Authentication Transactions',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The roles this user belongs to. A user will get all permissions granted to each of their roles.', related_name='user_set', related_query_name='user', to='users.Role', verbose_name='Roles'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]