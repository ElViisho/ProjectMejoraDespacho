# Generated by Django 4.0 on 2022-01-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0014_ordenes_numero_guia_alter_ordenes_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='documento_salida',
            field=models.FileField(default='None', upload_to='voucher_de_despacho/%Y/%m/%d/'),
        ),
    ]
