# Generated by Django 4.0.2 on 2022-02-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0022_ordenes_estado_pedido_para_vendedor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='estado_pedido_para_vendedor',
            field=models.IntegerField(choices=[(0, 'En Preparación'), (1, 'Detenido'), (2, 'Preparado incompleto'), (3, 'Preparado completo')], default=0),
        ),
    ]
