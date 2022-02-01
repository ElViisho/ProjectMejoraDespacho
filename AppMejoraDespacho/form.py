from django import forms
from AppMejoraDespacho.models import *
from django.forms.widgets import NumberInput

from django.db import connections
import datetime 
from .choices import comunas_longest, horas, regiones, choices_dispatch_way
from .queries import query_get_relevant_NVVs

from file_resubmit.admin import AdminResubmitFileWidget
from phonenumber_field.formfields import PhoneNumberField

def validate_file(file):
    '''
    Function for validating the size and extension of the submitted file.
    If the conditions are not met, it raises a ValidationError.
    '''
    valid_extension = ["png", "jpg", "pdf", "jpeg", "pjp", "pjpeg", "jfif"]
    size = file.size
    name = file.name.split(".")
    extension = name[len(name)-1].lower()
    # Validate the file extension
    if (extension not in valid_extension):
        raise forms.ValidationError("Error en el campo de comprobante de pago: extensión no valida (tiene que ser png, jpg o pdf), subió uno: " + extension)
    # Validate size less than 5MB so the database doesn't colapse
    if(size > 5283920 or size < 0):
        raise forms.ValidationError("Error en el campo de comprobante de pago: tamaño del archivo supera los límites, tiene que ser menor que 5 MB, subió uno de: " + str(size))

# Return all rows from a cursor as a dict
def dictfetchall(cursor):
    d = cursor.fetchall()
    nvvs = [('0', '-------------')]
    for i in range(len(d)):
        nvvs.append((str(i+1), d[i][0]))
    return tuple(nvvs)

# Get all the NVVs that are relevant and are not already submitted
def get_nvvs():
    on_base = Ordenes.objects.values('nvv')
    uwu = ['', '']
    for i in on_base:
        uwu.append(i['nvv'])
    cursor = connections['dimaco'].cursor()
    cursor.execute(query_get_relevant_NVVs.format(tuple(uwu)))
    return dictfetchall(cursor)

# Get the next valid day for dispatch (n day from now, if it's a weekend, get to monday)
def now_plus_n(n):
    dia = datetime.date.today() + datetime.timedelta(days=n)
    while (dia.weekday() in [5,6]):
        dia += datetime.timedelta(days=1)
    return dia

# Form for submitting a new order to the database
class ingresoForm(forms.Form):
    nvv = forms.ChoiceField(label='NVV', choices=get_nvvs, initial=0, required=True)
    tipo_despacho = forms.ChoiceField(label = 'Tipo de despacho', choices=choices_dispatch_way, initial=0, required=False, widget=forms.RadioSelect)
    despacho_externo = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre transporte'}))
    direccion_despacho_externo = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder': 'Dirección transporte'}))
    region = forms.ChoiceField(label='Región de despacho', choices=regiones, initial=0, required=False)
    comuna = forms.ChoiceField(label='Comuna de despacho', choices=comunas_longest, initial=0, required=False)
    direccion = forms.CharField(label='Dirección de despacho', max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Santa Elena 1596'}))
    cont_nombre = forms.CharField(label='Nombre contacto de despacho', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'José González'}))
    cont_telefono = PhoneNumberField(label='Teléfono contacto de despacho', required=True, error_messages={'invalid':'Error en el campo Teléfono: ingrese un valor válido (ej.: 987654321 o +56987654321 en caso de ser chileno)'}, widget=forms.TextInput(attrs={'placeholder': '987654321'}))
    comprobante_pago = forms.FileField(label='Comprobante de pago (opcional)', required=False, validators=[validate_file], widget=AdminResubmitFileWidget(attrs={"accept":"image/png, image/jpg, image/jpeg, application/pdf"}))
    now = datetime.datetime.now() # Get now time
    n=2 # Add two days from now to dispatch date
    if (now.hour >= 16):
        n = 3 # If time is past 4pm, add 3 days
    fecha_despacho = forms.DateField(label='Fecha de despacho', widget=NumberInput(attrs={'type': 'date', 'min': str(now_plus_n(n))}), required=True, initial=(now_plus_n(n)))

    # Get all dispatch time ranges and only put the possible values for selection
    hora_despacho_inicio = forms.ChoiceField(label='Rango horario de despacho', choices=horas[:-1], initial=8, required=True)
    hora_despacho_fin = forms.ChoiceField(label='', choices=horas[1:], initial=9, required=True)
    horas_extra_inicio = [("0", "-------")]
    for i in horas[2:-1]:
        horas_extra_inicio.append(i)
    horas_extra_inicio = tuple(horas_extra_inicio)
    hora_despacho_extra_inicio = forms.ChoiceField(label='Hora de despacho extra', choices=horas_extra_inicio, initial=0)
    horas_extra_fin = [("0", "-------")]
    for i in horas[3:]:
        horas_extra_fin.append(i)
    horas_extra_fin = tuple(horas_extra_fin)
    hora_despacho_extra_fin = forms.ChoiceField(label='', choices=horas_extra_fin, initial=0)

    observaciones = forms.CharField(label="Observaciones", required = False, widget=forms.Textarea(attrs={"rows":5, "cols":20, "placeholder": "Ingrese alguna observación en caso de ser pertinente"}))

    # Add new init method so that the get_nvv function is recalled everytime so that it is updated with the latest data
    def __init__(self, *args, **kwargs):
        super(ingresoForm, self).__init__(*args, **kwargs)
        self.nvv = get_nvvs()
        self.fields['nvv'].choices = self.nvv


    def clean_nvv(self):
        '''
        Method for validating the nvv field
        '''
        # Since it is a selection, it returns an index, so here it gets the value of that index
        i = self.cleaned_data['nvv']
        nvv_choices = self.nvv
        return nvv_choices[int(i)][1]

    def clean_fecha_despacho(self):
        '''
        Method for validating the dispatch date field is not on weekends
        '''
        d = self.cleaned_data['fecha_despacho']
        if (d.weekday() in [5,6]):
            raise forms.ValidationError("Error en el campo Fecha de despacho: No se puede despachar los fin de semana")
        return d

    def clean_hora_despacho_extra_fin(self):
        '''
        Method for validating the hour ranges
        '''
        inicio = self.cleaned_data['hora_despacho_inicio']
        fin = self.cleaned_data['hora_despacho_fin']
        if (int(fin) - int(inicio) < 1):
            raise forms.ValidationError("Error en el campo Hora de despacho: ingrese un rango horario válido")
        inicio_extra = self.cleaned_data['hora_despacho_extra_inicio']
        fin_extra = self.cleaned_data['hora_despacho_extra_fin']
        # Checks that the end hour of the range is at least one hour greater that the start hour
        # and that the second range is after the first
        if((int(inicio_extra) != 0) and (int(fin_extra) != 0) and ((int(fin_extra) - int(inicio_extra) < 1) or ((int(inicio_extra) - int(fin) < 1)))):
            raise forms.ValidationError("Error en el campo Hora de despacho: ingrese un rango horario válido")
        if(((int(inicio_extra) == 0) and (int(fin_extra) != 0)) or (int(inicio_extra) != 0) and (int(fin_extra) == 0)):
            raise forms.ValidationError("Error en el campo Hora de despacho: ingrese un rango horario válido")
        return fin_extra

class editFileForm(forms.Form):
    nuevo_comprobante_pago = forms.FileField(required=True, validators=[validate_file],)
    nvv_for_submit = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'style': 'display: none;'}))

    # Add new init method to add the attrs to the field
    def __init__(self, *args, **kwargs):
        super(editFileForm, self).__init__(*args, **kwargs)
        self.fields['nuevo_comprobante_pago'].widget.attrs.update({"accept":"image/png, image/jpg, image/jpeg, application/pdf", "onchange":"enable_button()"})

# Form for deleting an order from the database
class deleteForm(forms.Form):
    nvv = forms.ChoiceField(label='Eliga una NVV para eliminar', choices=(), required=True)

    def __init__(self, *args, **kwargs):
        super(deleteForm, self).__init__(*args, **kwargs)
        queryset = Ordenes.objects.all()
        choices_nvv = [("None", "----------")]
        for i in queryset:
            choices_nvv.append((i,i))
        self.fields['nvv'].choices = choices_nvv