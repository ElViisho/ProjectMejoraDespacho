# Generated by Django 4.0 on 2022-01-13 14:53

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('AppMejoraDespacho', '0011_ordenes_hora_despacho_extra_fin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='telefono_contacto',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
