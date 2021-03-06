# Generated by Django 4.0 on 2022-01-17 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0013_remove_ordenes_fecha_entregado_remove_ordenes_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenes',
            name='numero_guia',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='estado',
            field=models.IntegerField(choices=[(0, 'En Preparación'), (1, 'Preparado'), (2, 'Tubos'), (3, 'Cañería'), (4, 'Rollos')], default=0),
        ),
    ]
