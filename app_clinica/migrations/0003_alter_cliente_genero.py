# Generated by Django 4.2.1 on 2023-05-25 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_clinica', '0002_alter_cliente_genero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='genero',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_clinica.genero'),
        ),
    ]