# Generated by Django 4.0 on 2022-01-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pvmodels',
            name='id',
        ),
        migrations.AlterField(
            model_name='pvmodels',
            name='sku',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]