from django.db import models
from .choices import choices_estados, choices_estados_pedido_para_vendedor, choices_am_pm
from phonenumber_field.modelfields import PhoneNumberField

# Base model where all orders are stored with all of its data
# Only one was made because all ids have exactly one value for everything (for now, it may or may not change in the future)
class Ordenes(models.Model):
    nvv = models.CharField(max_length = 20, primary_key=True)
    fecha_nvv = models.DateField(db_index=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, db_index=True)
    rut = models.CharField(max_length=13, db_index=True)
    cliente = models.CharField(max_length=200, db_index=True)
    tipo_despacho = models.CharField(max_length=200, default="DIMACO")
    comuna = models.CharField(max_length=250, db_index=True)
    direccion = models.CharField(max_length=250)
    nombre_contacto = models.CharField(max_length=200)
    telefono_contacto = PhoneNumberField(null=False, blank=False)
    condicion_pago = models.CharField(max_length=100)
    comprobante_pago = models.FileField(upload_to='comprobantes_de_pago/%Y/%m/%d/', blank=True)
    observacion = models.CharField(max_length=2500, blank=True)
    fecha_despacho = models.DateField(db_index=True)
    fecha_despacho_final = models.DateField(db_index=True)
    hora_de_despacho_inicio = models.TimeField()
    hora_de_despacho_fin = models.TimeField()
    hora_despacho_extra_inicio = models.TimeField()
    hora_despacho_extra_fin = models.TimeField()
    rango_horario_final = models.IntegerField(default=0, choices=choices_am_pm)

    estado = models.IntegerField(default=0, choices=choices_estados)
    observacion_despacho = models.CharField(max_length=2500, blank=True)
    numero_guia = models.CharField(max_length=100, blank=True)
    documento_salida = models.FileField(upload_to='voucher_de_despacho/%Y/%m/%d/', default='None')

    nombre_vendedor = models.CharField(max_length=200, db_index=True)
    nombre_asistente = models.CharField(max_length=200, db_index=True)

    listo = models.IntegerField(default=0, choices=((0, "No"),(1, "Si")))

    estado_pedido_para_vendedor = models.IntegerField(default=0, choices=choices_estados_pedido_para_vendedor)

    valor_neto_documento = models.IntegerField(default=0)

    def __str__(self):
        return self.nvv
