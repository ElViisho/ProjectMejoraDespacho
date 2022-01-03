from django.db import models

class ordenes(models.Model):
    choices_estados = (
        (0, 'En Preparación'),
        (1, 'Preparado'),
        (2, 'Despachado')
    )
    choices_completo = (
        (0, 'No'),
        (1, 'Si')
    )
    nvv = models.CharField(primary_key=True)
    fecha_nvv = models.DateField(db_index=True)
    fecha_solicitud = models.DateField(auto_now_add=True, db_index=True)
    rut = models.CharField(max_length=12, db_index=True)
    cliente = models.CharField(db_index=True)
    direccion = models.CharField()
    comuna = models.CharField(db_index=True)
    nombre_contacto = models.CharField()
    telefono_contacto = models.CharField()
    condicion_pago = models.CharField()
    comprobante_pago = models.FileField(upload_to='comprobantes_de_pago/%Y/%m/%d/', blank=True)
    observacion = models.CharField(blank=True)
    fecha_despacho = models.DateField(db_index=True)
    hora_de_despacho = models.TimeField(db_index=True)

    fecha_entregado = models.DateField(db_index=True, blank=True)
    estado = models.IntegerField(default=0, choices=choices_estados)
    completado = models.IntegerField(default=0, choices=choices_completo)
    observacion_despacho = models.CharField(blank=True)
    documento_salida = models.FileField(upload_to='documentos_de_salida/%Y/%m/%d/', blank=True)
    numero = models.IntegerField(db_index=True)
