from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppMejoraDespacho.models import *
import re
from django.forms.widgets import NumberInput

from django.db import connections
import datetime 
from .choices import regiones, comunas, horas
from .consultas import consulta_NVVs

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
    cursor = connections['dimaco'].cursor()
    cursor.execute(consulta_NVVs)
    return dictfetchall(cursor)

class ingresoForm(forms.Form):
    nvv_choices = get_nvvs()
    nvv = forms.ChoiceField(label='NVV', choices=nvv_choices, initial=1, required=True)
    region = forms.ChoiceField(label = 'Región', choices=regiones, initial=7, required=True)
    comuna = forms.ChoiceField(label='Comuna', choices=comunas[6], initial=1, required=True)
    direccion = forms.CharField(label='Dirección', max_length=250, required=True)
    cont_nombre = forms.CharField(label='Nombre contacto', max_length=200, required=True)
    cont_telefono = forms.CharField(label='Teléfono contacto', max_length=12, required=True)
    comprobante_pago = forms.FileField(label='Comprobante de pago', required=False, validators=[validar_archivo])
    observaciones = forms.CharField(label="Observaciones", required = False, widget=forms.Textarea(attrs={"rows":5, "cols":20, "placeholder": "Ingrese alguna observación en caso de ser pertinente"}))
    fecha_despacho = forms.DateField(label='Fecha de despacho', widget=NumberInput(attrs={'type': 'date'}), required=True, initial=(datetime.date.today() + datetime.timedelta(days=2)))

    hora_despacho_inicio = forms.ChoiceField(label='Hora de despacho', choices=horas, initial=datetime.datetime.now().hour, required=True)
    hora_despacho_fin = forms.ChoiceField(label='', choices=horas, initial=datetime.datetime.now().hour + 1, required=True)

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