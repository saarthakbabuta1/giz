# Generated by Django 4.0 on 2022-01-16 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_mobile_alter_contact_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'contact Us', 'verbose_name_plural': 'Contact Us'},
        ),
    ]
