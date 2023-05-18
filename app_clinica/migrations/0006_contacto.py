# Generated by Django 4.2.1 on 2023-05-18 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_clinica', '0005_agendamiento_peluquera_alter_agendamiento_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=50)),
                ('asunto', models.CharField(max_length=50)),
                ('mensaje', models.TextField()),
            ],
        ),
    ]