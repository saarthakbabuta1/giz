# Generated by Django 4.0 on 2022-01-16 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_suryamitraprofile_user'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersmodel',
            name='ca_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='delivery_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='delivery_timeline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='discom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='order_confirmation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='suryamitra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.suryamitraprofile'),
        ),
        migrations.AddField(
            model_name='ordersmodel',
            name='tech_contact_information',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]