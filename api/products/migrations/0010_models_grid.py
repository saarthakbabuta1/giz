# Generated by Django 4.0 on 2022-01-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_products_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='models',
            name='grid',
            field=models.CharField(blank=True, choices=[('Off Grid', 'Off Grid'), ('On Grid', 'On Grid')], max_length=255, null=True),
        ),
    ]
