from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppMejoraDespacho.models import *
import re
from django.forms.widgets import NumberInput

from django.db import connections
import datetime 
from .choices import choices_estados, regiones, comunas, horas
from .consultas import consulta_NVVs

from file_resubmit.admin import AdminResubmitFileWidget

def validar_archivo(archivo):
    '''
    Funcion que validara el tamaño y la extensión del archivo que se subira.
    Esta estara presente en la clase IngresoForm como validador del campo comprobante_pago.
    Solo levantara un ValidationError si no cumple las condiciones impuestas.

    Inputs:
        archivo: Un objeto de la clase File de Django
    
    '''
    valid_extension = ["png", "jpg", "pdf"]
    size = archivo.size
    name = archivo.name.split(".")
    extension = name[len(name)-1].lower()
    if (extension not in valid_extension):
        raise forms.ValidationError("Error en el campo de comprobante de pago: extensión no valida (tiene que ser png, jpg o pdf), subió uno: " + extension)
    if(size > 3145728 or size < 0):
        raise forms.ValidationError("Error en el campo de comprobante de pago: tamaño del archivo supera los límites, tiene que ser menor que 3 MB, subió uno de: " + str(size))

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

class ingresoForm(forms.Form):
    nvv_choices = get_nvvs()
    nvv = forms.ChoiceField(label='NVV', choices=nvv_choices, initial=1, required=True)
    region = forms.ChoiceField(label = 'Región', choices=regiones, initial=7, required=True)
    comuna = forms.ChoiceField(label='Comuna', choices=comunas[6], initial=1, required=True)
    direccion = forms.CharField(label='Dirección', max_length=250, required=True)
    cont_nombre = forms.CharField(label='Nombre contacto', max_length=200, required=True)
    cont_telefono = forms.CharField(label='Teléfono contacto', max_length=12, required=True)
    comprobante_pago = forms.FileField(label='Comprobante de pago', required=False, validators=[validar_archivo], widget=AdminResubmitFileWidget())
    observaciones = forms.CharField(label="Observaciones", required = False, widget=forms.Textarea(attrs={"rows":5, "cols":20, "placeholder": "Ingrese alguna observación en caso de ser pertinente"}))
    fecha_despacho = forms.DateField(label='Fecha de despacho', widget=NumberInput(attrs={'type': 'date', 'min': str(datetime.date.today())}), required=True, initial=(datetime.date.today() + datetime.timedelta(days=2)))

    hora_despacho_inicio = forms.ChoiceField(label='Hora de despacho', choices=horas, initial=8, required=True)
    hora_despacho_fin = forms.ChoiceField(label='', choices=horas, initial=9, required=True)

    def __init__(self, *args, **kwargs):
        super(ingresoForm, self).__init__(*args, **kwargs)
        self.fields['nvv'].choices = get_nvvs()
        self.fields['fecha_despacho'].initial = datetime.date.today() + datetime.timedelta(days=2)

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
            raise forms.ValidationError("Error con el campo Hora de despacho: ingrese un rango horario válido")

        fecha = (self.cleaned_data['fecha_despacho'])
        if (fecha == datetime.date.today() and ((datetime.datetime.now().hour > int(inicio)) or (datetime.datetime.now().hour > int(fin)))):
            raise forms.ValidationError("Error con el campo Hora de despacho: rango horario en el pasado")
        return fin

    def clean_cont_telefono(self):
        '''
        Metodo que validara el campo de telefono
        '''
        dato = self.cleaned_data['cont_telefono']
        regex = re.compile(r'(\+?[0-9]+)')
        if(regex.fullmatch(dato) is None):
            raise forms.ValidationError("Error con el campo Teléfono: número de teléfono inválido")
        return dato


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
            raise forms.ValidationError("Error con el campo Fecha de entrega: ingrese un valor")
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