# Generated by Django 4.0 on 2022-01-03 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_pvmodels_id_alter_pvmodels_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='PvProducts',
            fields=[
                ('sku', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('oem', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('assembly', models.TextField()),
                ('comments', models.TextField()),
                ('sku_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.pvmodels')),
            ],
            options={
                'db_table': 'pv_products',
            },
        ),
    ]
