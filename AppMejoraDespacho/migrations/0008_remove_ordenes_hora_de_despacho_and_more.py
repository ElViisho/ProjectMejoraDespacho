# Generated by Django 4.0 on 2022-01-07 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0007_alter_ordenes_fecha_entregado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenes',
            name='hora_de_despacho',
        ),
        migrations.AddField(
            model_name='ordenes',
            name='hora_de_despacho_fin',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenes',
            name='hora_de_despacho_inicio',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
