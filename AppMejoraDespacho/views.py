
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from AppMejoraDespacho.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connections

from AppMejoraDespacho.form import ingresoForm
import datetime
from django.db import connections

from .choices import regiones, comunas

def inicio(request):
	'''
	Funcion para mostrar el html inicio de la aplicacion con render
	Pagina: inicio
	'''
	return render(request, "AppMejoraDespacho/inicio.html")


def ingresar(request):
	if request.method == 'GET':
		formulario = ingresoForm()
		for field in formulario:
			field.field.widget.attrs.update({"class": "form-control"})
		return render(request, "AppMejoraDespacho/form.html", {"formulario": formulario})
	if request.method == "POST":
		data_obtenida = ingresoForm(request.POST or None, request.FILES or None)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			nvv = cleaned_data['nvv']

			if cleaned_data['comprobante_pago'] is None:
				cleaned_data['comprobante_pago'] = "None"

			cursor = connections['dimaco'].cursor()
			cursor.execute("SELECT * FROM [DIMACO_NEW].[dbo].[MAEEDO] WHERE NUDO = %s AND TIDO = 'NVV';", [nvv])
			datos_maeedo = dictfetchall(cursor)

			cursor.execute("""SELECT * FROM [DIMACO_NEW].[dbo].[MAEEN]
							INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEN].[KOEN] = [DIMACO_NEW].[dbo].[MAEEDO].[ENDO]
							WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = (
								SELECT [NUDO] 
								FROM [DIMACO_NEW].[dbo].[MAEEDO] 
								WHERE NUDO = %s AND TIDO = 'NVV') AND [DIMACO_NEW].[dbo].[MAEEN].[TIPOSUC]='P';""", [nvv])
			datos_maeen = dictfetchall(cursor)

			cursor.execute("""SELECT * FROM [DIMACO_NEW].[dbo].[MAEEDOOB]
							INNER JOIN [DIMACO_NEW].[dbo].[MAEEDO] on [DIMACO_NEW].[dbo].[MAEEDOOB].[IDMAEEDO] = [DIMACO_NEW].[dbo].[MAEEDO].[IDMAEEDO]
							WHERE [DIMACO_NEW].[dbo].[MAEEDO].[NUDO] = (
								SELECT [NUDO]
								FROM [DIMACO_NEW].[dbo].[MAEEDO] 
								WHERE NUDO = %s AND TIDO = 'NVV');""", [nvv])
			datos_maeedoob = dictfetchall(cursor)

			Ordenes.objects.create(
				nvv = nvv,
				fecha_nvv = datos_maeedo[0]["FEEMDO"],
				rut = datos_maeedo[0]["ENDO"],
				cliente = datos_maeen[0]["NOKOEN"],
				region = cleaned_data['region'],
				comuna = cleaned_data['comuna'],
				direccion = cleaned_data['direccion'],
				nombre_contacto = cleaned_data['cont_nombre'],
				telefono_contacto = cleaned_data['cont_telefono'],
				condicion_pago = datos_maeedoob[0]["OBDO"],
				comprobante_pago = cleaned_data['comprobante_pago'],
				observacion = cleaned_data['observaciones'],
				fecha_despacho = cleaned_data['fecha_despacho'],
				hora_de_despacho_inicio = datetime.time(hour=int(cleaned_data['hora_despacho_inicio'])),
				hora_de_despacho_fin = datetime.time(hour=int(cleaned_data['hora_despacho_fin'])),
			)
			return redirect("confirm_nvv")
		return render(request, "AppMejoraDespacho/form.html", {"formulario": data_obtenida})


def confirm_nvv(request):
	'''
	Funcion de mostrar la pagina de exitoso ingreso de la nota de venta a la base
	'''
	return render(request, "AppMejoraDespacho/confirm_nvv.html")

def modificar_nvv(request):
	'''
	Funcion de mostrar la pagina para modificar una nota de venta de la base
	'''
	queryset = Ordenes.objects.all()
	return render(request, "AppMejoraDespacho/modificar_nvv.html", {"queryset": queryset,})

def tabla(request):
	'''
	Funcion de mostrar la pagina con la tabla de la base de datos
	'''
	queryset = Ordenes.objects.all()
	return render(request, "AppMejoraDespacho/tabla.html",{"queryset": queryset, "regiones": regiones, "comunas": comunas})

def load_comunas(request):
    region = request.GET.get('region')
    com = comunas[int(region)-1]
    return render(request, 'AppMejoraDespacho/comuna_dropdown_list_options.html', {'comunas': com})

def pa_probar(request):
	cursor = connections['dimaco'].cursor()
	cursor.execute("SELECT TOP (10) * FROM [DIMACO_NEW].[dbo].[MAEEDO]")
	rows = dictfetchall(cursor)

	return render(request, "AppMejoraDespacho/pa_probar.html", {"base": rows})




def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]