# Generated by Django 4.0 on 2022-01-06 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_pvproducts_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PvModels',
            new_name='Models',
        ),
        migrations.RenameModel(
            old_name='PvProducts',
            new_name='Products',
        ),
    ]
