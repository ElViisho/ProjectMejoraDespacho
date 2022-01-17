from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppMejoraDespacho.models import *
import re, magic
from django.forms.widgets import NumberInput

from django.db import connections
import datetime 
from .choices import choices_estados, regiones, comunas, horas
from .consultas import consulta_NVVs

from file_resubmit.admin import AdminResubmitFileWidget
from phonenumber_field.formfields import PhoneNumberField

def validar_archivo(archivo):
    '''
    Funcion que validara el tamaño y la extensión del archivo que se subira.
    Esta estara presente en la clase IngresoForm como validador del campo comprobante_pago.
    Solo levantara un ValidationError si no cumple las condiciones impuestas.    
    '''

    valid_mime_types = ['application/pdf', 'image/png', 'image/jpeg']
    file_mime_type = magic.from_buffer(archivo.read(1024), mime=True)
    if file_mime_type not in valid_mime_types:
        raise forms.ValidationError("Error en el campo de comprobante de pago: tipo de archivo no valido (tiene que ser png, jpeg, jpg o pdf)")
    valid_extension = ["png", "jpg", "pdf", "jpeg", "pjp", "pjpeg", "jfif"]
    size = archivo.size
    name = archivo.name.split(".")
    extension = name[len(name)-1].lower()
    if (extension not in valid_extension):
        raise forms.ValidationError("Error en el campo de comprobante de pago: extensión no valida (tiene que ser png, jpg o pdf), subió uno: " + extension)
    if(size > 5283920 or size < 0):
        raise forms.ValidationError("Error en el campo de comprobante de pago: tamaño del archivo supera los límites, tiene que ser menor que 5 MB, subió uno de: " + str(size))

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    d = cursor.fetchall()
    nvvs = []
    for i in range(len(d)):
        nvvs.append((str(i+1), d[i][0]))
    return tuple(nvvs)

def get_nvvs():
    ya_en_la_base = Ordenes.objects.values('nvv')
    uwu = ['', '']
    for i in ya_en_la_base:
        uwu.append(i['nvv'])
    cursor = connections['dimaco'].cursor()
    cursor.execute(consulta_NVVs.format(tuple(uwu)))
    return dictfetchall(cursor)

def now_plus_n(n):
    return datetime.date.today() + datetime.timedelta(days=n)

class ingresoForm(forms.Form):
    nvv_choices = get_nvvs()
    nvv = forms.ChoiceField(label='NVV', choices=nvv_choices, initial=1, required=True)
    region = forms.ChoiceField(label = 'Región', choices=regiones, initial=7, required=True)
    comuna = forms.ChoiceField(label='Comuna', choices=comunas[6], initial=1, required=True)
    direccion = forms.CharField(label='Dirección', max_length=250, required=True)
    cont_nombre = forms.CharField(label='Nombre contacto de despacho', max_length=200, required=True)
    cont_telefono = PhoneNumberField(label='Teléfono contacto de despacho', required=True, error_messages={'invalid':'Error en el campo Teléfono: ingrese un valor válido (ej.: 987654321 o +56987654321)'})
    comprobante_pago = forms.FileField(label='Comprobante de pago (opcional)', required=False, validators=[validar_archivo], widget=AdminResubmitFileWidget(attrs={"accept":"image/png, image/jpg, image/jpeg, application/pdf"}))
    now = datetime.datetime.now()
    n=2
    if (now.hour >= 4):
        n = 3
    fecha_despacho = forms.DateField(label='Fecha de despacho', widget=NumberInput(attrs={'type': 'date', 'min': str(now_plus_n(n))}), required=True, initial=(now_plus_n(n)))

    hora_despacho_inicio = forms.ChoiceField(label='Hora de despacho', choices=horas, initial=8, required=True)
    hora_despacho_fin = forms.ChoiceField(label='', choices=horas, initial=9, required=True)
    horas_extra = [("0", "-------")]
    for i in horas:
        horas_extra.append(i)
    horas_extra = tuple(horas_extra)
    hora_despacho_extra_inicio = forms.ChoiceField(label='Hora de despacho extra', choices=horas_extra, initial=0)
    hora_despacho_extra_fin = forms.ChoiceField(label='', choices=horas_extra, initial=0)

    observaciones = forms.CharField(label="Observaciones", required = False, widget=forms.Textarea(attrs={"rows":5, "cols":20, "placeholder": "Ingrese alguna observación en caso de ser pertinente"}))

    def __init__(self, *args, **kwargs):
        super(ingresoForm, self).__init__(*args, **kwargs)
        self.fields['nvv'].choices = get_nvvs()

    def clean_nvv(self):
        i = self.cleaned_data['nvv']
        nvv_choices = get_nvvs()
        return nvv_choices[int(i)-1][1]

    def clean_hora_despacho_fin(self):
        '''
        Metodo que validara los campos de la hora
        '''
        inicio = self.cleaned_data['hora_despacho_inicio']
        fin = self.cleaned_data['hora_despacho_fin']
        if(int(fin) - int(inicio) < 1):
            raise forms.ValidationError("Error en el campo Hora de despacho: ingrese un rango horario válido")

        fecha = (self.cleaned_data['fecha_despacho'])
        if (fecha == datetime.date.today() and ((datetime.datetime.now().hour > int(inicio)) or (datetime.datetime.now().hour > int(fin)))):
            raise forms.ValidationError("Error en el campo Hora de despacho: rango horario en el pasado")
        return fin

    def clean_hora_despacho_extra_fin(self):
        '''
        Metodo que validara los campos de la hora extra
        '''
        try:
            fin = self.cleaned_data['hora_despacho_fin']
            inicio_extra = self.cleaned_data['hora_despacho_extra_inicio']
            fin_extra = self.cleaned_data['hora_despacho_extra_fin']
            if((int(fin_extra) - int(inicio_extra) < 1) or ((int(inicio_extra) - int(fin) < 1))):
                raise forms.ValidationError("Error en el campo Hora de despacho: ingrese un rango horario válido")
            return fin_extra
        except:
            return self.cleaned_data['hora_despacho_extra_fin']


class modifyForm(forms.Form):
    nvv = forms.ChoiceField(label='NVV', choices=(), required=True)
    estado = forms.ChoiceField(label = 'Estado', choices=choices_estados, initial=0, required=True)
    fecha_entregado = forms.DateField(label='Fecha de despacho', widget=NumberInput(attrs={'type': 'date'}), required=False)
    observacion_despacho = forms.CharField(label='Observaciones de entrega', required = False, widget=forms.Textarea(attrs={"rows":5, "cols":20, "placeholder": "Ingrese alguna observación en caso de ser pertinente"}))

    def __init__(self, *args, **kwargs):
        super(modifyForm, self).__init__(*args, **kwargs)
        queryset = Ordenes.objects.all()
        choices_nvv = [("None", "----------")]
        for i in queryset:
            choices_nvv.append((i,i))
        self.fields['nvv'].choices = choices_nvv

    def clean_fecha_entregado(self):
        '''
        Metodo que validara el campo de la fecha que se entregó el paquete
        '''
        estado = self.cleaned_data['estado']
        if (estado != '2'): return None
        fecha_entregado = self.cleaned_data['fecha_entregado']
        if(fecha_entregado is None):
            raise forms.ValidationError("Error en el campo Fecha de entrega: ingrese un valor")
        return fecha_entregado

class deleteForm(forms.Form):
    nvv = forms.ChoiceField(label='Eliga una NVV para eliminar', choices=(), required=True)

    def __init__(self, *args, **kwargs):
        super(deleteForm, self).__init__(*args, **kwargs)
        queryset = Ordenes.objects.all()
        choices_nvv = [("None", "----------")]
        for i in queryset:
            choices_nvv.append((i,i))
        self.fields['nvv'].choices = choices_nvv