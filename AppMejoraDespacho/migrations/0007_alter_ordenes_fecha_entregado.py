# Generated by Django 4.0 on 2022-01-06 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0006_alter_ordenes_fecha_entregado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='fecha_entregado',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
    ]
