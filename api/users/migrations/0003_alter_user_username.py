# Generated by Django 4.0 on 2022-01-01 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_otpvalidation_user_date_joined_user_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=254, unique=True, verbose_name='Username'),
        ),
    ]
