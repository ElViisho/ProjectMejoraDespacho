
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from AppMejoraDespacho.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from AppMejoraDespacho.form import ingresoForm
import datetime

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

			if cleaned_data['comprobante_pago'] is None:
				print("xd")
				cleaned_data['comprobante_pago'] = "None"

			Ordenes.objects.create(
				nvv = cleaned_data['nvv'],
				fecha_nvv = datetime.date.today(), #CAMBIAAAAR
				rut = 0, #CAMBIAAAAR
				cliente = "k", #CAMBIAAAR
				direccion = cleaned_data['direccion'],
				comuna = cleaned_data['comuna'],
				nombre_contacto = cleaned_data['cont_nombre'],
				telefono_contacto = cleaned_data['cont_telefono'],
				condicion_pago = "xd", #CAMBIAAAAR
				comprobante_pago = cleaned_data['comprobante_pago'],
				observacion = cleaned_data['observaciones'],
				fecha_despacho = cleaned_data['fecha_despacho'],
				hora_de_despacho = cleaned_data['hora_despacho']
			)
			return redirect("confirm_nvv")
		return render(request, "AppMejoraDespacho/form.html", {"formulario": data_obtenida})


def confirm_nvv(request):
	'''
	Funcion de mostrar la pagina de exitoso ingreso de la nota de venta a la base
	'''
	return render(request, "AppMejoraDespacho/confirm_nvv.html")

def tabla(request):
	'''
	Funcion de mostrar la pagina con la tabla de la base de datos
	'''
	base = Ordenes.objects.all()
	return render(request, "AppMejoraDespacho/tabla.html",{"queryset": base})