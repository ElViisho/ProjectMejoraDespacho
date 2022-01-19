
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

from AppMejoraDespacho.form import ingresoForm, deleteForm
import datetime
from django.db import connections

from django.core import serializers
import json

from .choices import regiones, comunas
from .consultas import *

import time

def loginPage(request):
	'''
	Funcion para mostrar la pagina de login de la app
	Pagina: login
	'''
	context = {}
	if request.user.is_authenticated:
		return redirect('inicio')
	
	else:
		if request.method  == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('inicio')
			else:
				context = {"error":" Usuario y/o contraseña incorrecta, vuelva a intentarlo"}

		
		return render(request, "AppMejoraDespacho/login.html", context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def inicio(request):
	'''
	Funcion para mostrar el html inicio de la aplicacion con render
	Pagina: inicio
	'''
	grupos = list(request.user.groups.values_list('name', flat= True))
	permisos = 'Básico'
	if (len(grupos) > 0):
		permisos = grupos[0]
	if request.user.is_superuser:
		permisos = 'Eliminar'
	return render(request, "AppMejoraDespacho/inicio.html", {"permisos": permisos})

@login_required(login_url='login')
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
			cursor.execute(consulta_maeedo, [nvv])
			datos_maeedo = dictfetchall(cursor)

			cursor.execute(consulta_maeen, [nvv])
			datos_maeen = dictfetchall(cursor)

			cursor.execute(consulta_maeedoob, [nvv])
			datos_maeedoob = dictfetchall(cursor)

			cursor.execute(consulta_tabfu, [nvv])
			datos_tabfu = dictfetchall(cursor)

			Ordenes.objects.create(
				nvv = nvv,
				fecha_nvv = datos_maeedo[0]["FEEMDO"],
				nombre_vendedor = datos_tabfu[0]["NOKOFU"],
				rut = datos_maeedo[0]["ENDO"],
				cliente = datos_maeen[0]["NOKOEN"],
				region = cleaned_data['region'],
				comuna = cleaned_data['comuna'],
				direccion = cleaned_data['direccion'],
				nombre_contacto = cleaned_data['cont_nombre'],
				telefono_contacto = cleaned_data['cont_telefono'],
				condicion_pago = datos_maeedoob[0]["CPDO"],
				comprobante_pago = cleaned_data['comprobante_pago'],
				observacion = cleaned_data['observaciones'],
				fecha_despacho = cleaned_data['fecha_despacho'],
				hora_de_despacho_inicio = datetime.time(hour=int(cleaned_data['hora_despacho_inicio'])),
				hora_de_despacho_fin = datetime.time(hour=int(cleaned_data['hora_despacho_fin'])),
				hora_despacho_extra_inicio = datetime.time(hour=int(cleaned_data['hora_despacho_extra_inicio'])),
				hora_despacho_extra_fin = datetime.time(hour=int(cleaned_data['hora_despacho_extra_fin'])),
				nombre_asistente = request.user.get_full_name(),
				valor_neto_documento = datos_maeedo[0]["VANEDO"],
			)		
			return redirect("confirm_nvv")
		return render(request, "AppMejoraDespacho/form.html", {"formulario": data_obtenida})

@login_required(login_url='login')
def confirm_nvv(request):
	'''
	Funcion de mostrar la pagina de exitoso ingreso de la nota de venta a la base
	'''
	return render(request, "AppMejoraDespacho/confirm_nvv.html")

@login_required(login_url='login')
def delete_nvv(request):
	'''
	Funcion de mostrar la pagina para eliminar una nota de venta de la base
	'''
	if (not request.user.is_superuser and list(request.user.groups.values_list('name', flat= True))[0] != 'Eliminar'):
		return redirect('inicio')
	if request.method == 'GET':
		formulario = deleteForm()
		for field in formulario:
			field.field.widget.attrs.update({"class": "form-control"})
		return render(request, "AppMejoraDespacho/delete_nvv.html", {"formulario": formulario})
	if request.method == "POST":
		data_obtenida = deleteForm(request.POST or None)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			Ordenes.objects.filter(nvv=cleaned_data['nvv']).delete()
			return redirect("confirm_delete_nvv")
		return render(request, "AppMejoraDespacho/delete_nvv.html", {"formulario": data_obtenida})

@login_required(login_url='login')
def confirm_delete_nvv(request):
	'''
	Funcion de mostrar la pagina de exitoso ingreso de la nota de venta a la base
	'''
	return render(request, "AppMejoraDespacho/confirm_delete_nvv.html")

@login_required(login_url='login')
def tabla_modificable_con_guia(request):
	con_guia = "True"
	return tabla_modificable(request, con_guia)

@login_required(login_url='login')
def tabla_modificable_sin_guia(request):
	con_guia = "False"
	return  tabla_modificable(request, con_guia)

def tabla_modificable(request, con_guia):
	'''
	Funcion de mostrar la pagina con la tabla modificable de la base de datos
	'''
	queryset = Ordenes.objects.all()
	
	if request.method == "POST":
		data = request.POST
		if (data['type'] == 'estado'):
			Ordenes.objects.filter(nvv=data['nvv']).update(estado=data['option'])
		elif (data['type'] == 'numero_guia'):
			nvv = data['nvv']
			listo = 1-int(data['listo'])
			Ordenes.objects.filter(nvv=nvv).update(listo=listo)
			bool_n_guia = change_numero_guia(nvv, listo)
			if (not bool_n_guia):
				return 'error'
	
	grupos = list(request.user.groups.values_list('name', flat= True))
	permisos = 'Básico'
	if (len(grupos) > 0):
		permisos = grupos[0]
	if request.user.is_superuser:
		permisos = 'Despacho'
	return render(request, "AppMejoraDespacho/tabla_modificable.html",{"permisos": permisos, "queryset": queryset, "regiones": regiones, "comunas": comunas, "con_guia": con_guia,})

def change_numero_guia(nvv, listo):
	if not listo:
		Ordenes.objects.filter(nvv=nvv).update(numero_guia='')
		return True
	else:
		cursor = connections['dimaco'].cursor()
		cursor.execute(consulta_guia_despacho, [nvv])
		datos = dictfetchall(cursor)
		if datos:
			n_guia = datos[0]['TIDO']+' Número '+ datos[0]['NUDO']
			Ordenes.objects.filter(nvv=nvv).update(numero_guia=n_guia)
			return True
		else:
			Ordenes.objects.filter(nvv=nvv).update(listo=0)
			return False

def load_comunas(request):
    region = request.GET.get('region')
    com = comunas[int(region)-1]
    return render(request, 'AppMejoraDespacho/comuna_dropdown_list_options.html', {'comunas': com})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
