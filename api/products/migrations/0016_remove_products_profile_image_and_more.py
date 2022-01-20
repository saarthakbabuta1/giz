# Generated by Django 4.0 on 2022-01-20 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_remove_models_available_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='products',
            name='required_quanity',
        ),
        migrations.AlterField(
            model_name='products',
            name='oem',
            field=models.CharField(max_length=100, verbose_name='OEM'),
        ),
        migrations.AlterField(
            model_name='products',
            name='sku',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='SKU'),
        ),
    ]