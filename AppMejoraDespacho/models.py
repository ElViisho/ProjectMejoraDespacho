from django.db import models
from .choices import choices_estados, regiones
from phonenumber_field.modelfields import PhoneNumberField

class Ordenes(models.Model):
    nvv = models.CharField(max_length = 20, primary_key=True)
    fecha_nvv = models.DateField(db_index=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, db_index=True)
    rut = models.CharField(max_length=13, db_index=True)
    cliente = models.CharField(max_length=200, db_index=True)
    direccion = models.CharField(max_length=250)
    region = models.IntegerField(choices=regiones, db_index=True)
    comuna = models.CharField(max_length=50, db_index=True)
    nombre_contacto = models.CharField(max_length=200)
    telefono_contacto = PhoneNumberField(null=False, blank=False)
    condicion_pago = models.CharField(max_length=100)
    comprobante_pago = models.FileField(upload_to='comprobantes_de_pago/%Y/%m/%d/', blank=True)
    observacion = models.CharField(max_length=2500, blank=True)
    fecha_despacho = models.DateField(db_index=True)
    hora_de_despacho_inicio = models.TimeField()
    hora_de_despacho_fin = models.TimeField()
    hora_despacho_extra_inicio = models.TimeField()
    hora_despacho_extra_fin = models.TimeField()

    estado = models.IntegerField(default=0, choices=choices_estados)
    observacion_despacho = models.CharField(max_length=2500, blank=True)
    numero_guia = models.CharField(max_length=100, blank=True)
    documento_salida = models.FileField(upload_to='voucher_de_despacho/%Y/%m/%d/', default='None')

    nombre_vendedor = models.CharField(max_length=200, db_index=True)
    nombre_asistente = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.nvv
