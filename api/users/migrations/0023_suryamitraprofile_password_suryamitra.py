# Generated by Django 4.0 on 2022-01-19 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_vendorprofile_contact_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='suryamitraprofile',
            name='password_suryamitra',
            field=models.CharField(default='password@123', max_length=255, verbose_name='Profile Password'),
        ),
    ]
