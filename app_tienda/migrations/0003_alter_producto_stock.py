# Generated by Django 4.2 on 2023-05-10 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tienda', '0002_producto_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
