# Generated by Django 4.2.1 on 2023-05-31 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_clinica', '0008_alter_diagnostico_agendamiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agendamiento',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='agendamiento',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='agendamiento',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='agendamiento',
            name='rut',
        ),
    ]
