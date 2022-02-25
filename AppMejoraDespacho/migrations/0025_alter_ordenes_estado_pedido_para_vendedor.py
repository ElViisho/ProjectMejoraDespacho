# Generated by Django 4.0 on 2022-02-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0024_alter_ordenes_estado_pedido_para_vendedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='estado_pedido_para_vendedor',
            field=models.IntegerField(choices=[(0, 'En Preparación'), (1, 'Detenido'), (2, 'Preparado incompleto'), (3, 'Preparado completo'), (10, 'CREADO'), (11, 'LIBERADO'), (12, 'ANDEN'), (13, 'PICKING'), (14, 'DESPACHADO'), (15, 'ANULADO'), (16, 'ELIMINADO')], default=0),
        ),
    ]
