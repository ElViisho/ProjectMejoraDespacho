# Generated by Django 4.0 on 2022-01-14 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0012_alter_ordenes_telefono_contacto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenes',
            name='fecha_entregado',
        ),
        migrations.RemoveField(
            model_name='ordenes',
            name='numero',
        ),
    ]
