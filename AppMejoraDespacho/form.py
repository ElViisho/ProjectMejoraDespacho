from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppMejoraDespacho.models import *
import re


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


class ingresoForm(forms.Form):
    nvv = forms.CharField(label='NVV', max_length=20, required=True)
    direccion = forms.CharField(label='Dirección', max_length=250, required=True)
    comuna = forms.CharField(label='Comuna', max_length=50, required=True)
    cont_nombre = forms.CharField(label='Nombre contacto', max_length=200, required=True)
    cont_telefono = forms.CharField(label='Teléfono contacto', max_length=12, required=True)
    comprobante_pago = forms.FileField(label='Comprobante de pago', required=False, validators=[validar_archivo])
    observaciones = forms.CharField(label="Observaciones", required = False, widget=forms.Textarea(attrs={"rows":5, "cols":20, "placeholder": "Ingrese alguna observación en caso de ser pertinente"}))
    fecha_despacho = forms.DateField(label='Fecha de despacho', input_formats=['%d/%m/%Y'], required=True)
    hora_despacho = forms.TimeField(label='Hora de despacho', input_formats=['%H:%M'], required=True)

    def clean_nvv(self):
        '''
        Metodo que validara el campo de nvv
        '''
        dato = self.cleaned_data['nvv']
        regex = re.compile(r'(V[0-9]*)')
        if(regex.fullmatch(dato) is None):
            raise forms.ValidationError("Error con el campo NVV: ingrese formato correcto (V123456)")
        return dato

    def clean_cont_telefono(self):
        '''
        Metodo que validara el campo de telefono
        '''
        dato = self.cleaned_data['cont_telefono']
        regex = re.compile(r'(\+?[0-9]+)')
        if(regex.fullmatch(dato) is None):
            raise forms.ValidationError("Error con el campo Teléfono: número de teléfono inválido")
        return dato