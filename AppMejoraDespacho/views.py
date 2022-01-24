
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from AppMejoraDespacho.models import *
from django.contrib.auth.decorators import login_required
from django.db import connections

from AppMejoraDespacho.form import ingresoForm, deleteForm
import datetime
from django.db import connections

from .choices import comunas_santa_elena, comunas_todas, regiones
from .queries import *


def loginPage(request):
	'''
	Renders the login page
	Whenever a user is not logged in and tries to go to other directions, 
	it goes back to here inmediately
	Page: login
	'''
	context = {}
	if request.user.is_authenticated:
		return redirect('main')
	
	else:
		if request.method  == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)

			# If user is valid, go to main page
			if user is not None:
				login(request, user)
				return redirect('main')
			else:
				context = {"error":" Usuario y/o contraseña incorrecta, vuelva a intentarlo"}

		
		return render(request, "AppMejoraDespacho/login.html", context)

def logoutUser(request):
	'''
	Method that handles the logging out of the app
	It redirects to the login page afterwards
	Page: logout
	'''
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def main(request):
	'''
	Renders the base page of the app
	Page: main
	'''
	groups = list(request.user.groups.values_list('name', flat= True)) # Get user permissions to pass it to the template so it knows what to show
	permissions = 'Básico'
	if (len(groups) > 0):
		permissions = groups[0]
	# TEMPORARY, JUST FOR DEBUGGING WHEN SUPERUSER IS LOGGED IN TO HAVE ALL PERMISSIONS
	if request.user.is_superuser:
		permissions = 'Eliminar'
	return render(request, "AppMejoraDespacho/main.html", {"permissions": permissions})

@login_required(login_url='login')
def submit_nvv_form(request):
	'''
	Renders the form for submitting a new order
	Page: submit_nvv_form
	'''
	if request.method == 'GET':
		# Get form withut data and pass it to the renderer
		formulario = ingresoForm()
		for field in formulario:
			field.field.widget.attrs.update({"class": "form-control"})
		return render(request, "AppMejoraDespacho/submit_nvv_form.html", {"formulario": formulario})
	if request.method == "POST":
		# Get the data from the post into the form and validate it
		data_obtenida = ingresoForm(request.POST or None, request.FILES or None)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			nvv = cleaned_data['nvv']

			if cleaned_data['tipo_despacho'] == "1":
				tipo_despacho = cleaned_data['despacho_externo']
				comuna = comunas_todas[int(cleaned_data['region'])][int(cleaned_data['comuna'])-1][1] + ', ' + regiones[int(cleaned_data['region'])-1][1] 
			else:
				tipo_despacho = 'DIMACO'
				comuna = comunas_santa_elena[int(cleaned_data['comuna'])-1][1]

			if cleaned_data['comprobante_pago'] is None:
				cleaned_data['comprobante_pago'] = "None"

			# Queries for getting important data from the Random ERP database
			cursor = connections['dimaco'].cursor()
			cursor.execute(query_get_nvv_data, [nvv])
			datos_maeedo = dictfetchall(cursor)

			cursor.execute(query_get_client_name, [nvv])
			datos_maeen = dictfetchall(cursor)

			cursor.execute(query_get_payment_condition, [nvv])
			datos_maeedoob = dictfetchall(cursor)

			cursor.execute(query_get_seller_name, [nvv])
			datos_tabfu = dictfetchall(cursor)

			# Create a new object in this app's database with all the gathered data
			Ordenes.objects.create(
				nvv = nvv,
				fecha_nvv = datos_maeedo[0]["FEEMDO"],
				nombre_vendedor = datos_tabfu[0]["NOKOFU"],
				tipo_despacho = tipo_despacho,
				rut = datos_maeedo[0]["ENDO"],
				cliente = datos_maeen[0]["NOKOEN"],
				comuna = comuna,
				direccion = cleaned_data['direccion'],
				nombre_contacto = cleaned_data['cont_nombre'],
				telefono_contacto = cleaned_data['cont_telefono'],
				condicion_pago = datos_maeedoob[0]["CPDO"],
				comprobante_pago = cleaned_data['comprobante_pago'],
				observacion = cleaned_data['observaciones'],
				fecha_despacho = cleaned_data['fecha_despacho'],
				fecha_despacho_final = cleaned_data['fecha_despacho'],
				hora_de_despacho_inicio = datetime.time(hour=int(cleaned_data['hora_despacho_inicio'])),
				hora_de_despacho_fin = datetime.time(hour=int(cleaned_data['hora_despacho_fin'])),
				hora_despacho_extra_inicio = datetime.time(hour=int(cleaned_data['hora_despacho_extra_inicio'])),
				hora_despacho_extra_fin = datetime.time(hour=int(cleaned_data['hora_despacho_extra_fin'])),
				nombre_asistente = request.user.get_full_name(),
				valor_neto_documento = datos_maeedo[0]["VANEDO"],
			)		
			return redirect("confirm_nvv")
		# If data not valid, rerender the page and don't lose the data that was already there
		return render(request, "AppMejoraDespacho/submit_nvv_form.html", {"formulario": data_obtenida})

@login_required(login_url='login')
def confirm_nvv(request):
	'''
	Renders the page that confirms the succesful submitting of a new order
	Page: confirm_nvv
	'''
	return render(request, "AppMejoraDespacho/confirm_nvv.html")

@login_required(login_url='login')
def delete_nvv(request):
	'''
	Renders the form for deleting an order from the database
	Page: delete_nvv
	'''
	if (not request.user.is_superuser and list(request.user.groups.values_list('name', flat= True))[0] != 'Eliminar'):
		return redirect('main')
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
	Renders the page that confirms the succesful deleting of an order
	Page: confirm_delete_nvv
	'''
	return render(request, "AppMejoraDespacho/confirm_delete_nvv.html")

def table(request):
	'''
	Renders the table with all the current data present in the database
	'''
	queryset = Ordenes.objects.all() # Get the data from the database
	
	groups = list(request.user.groups.values_list('name', flat= True)) # Get user permissions to pass it to the template so it knows what to show
	permissions = 'Básico'
	if (len(groups) > 0):
		permissions = groups[0]
	# TEMPORARY, JUST FOR DEBUGGING WHEN SUPERUSER IS LOGGED IN TO HAVE ALL PERMISSIONS
	if request.user.is_superuser:
		permissions = 'Despacho'
	return render(request, "AppMejoraDespacho/table.html",{"permissions": permissions, "queryset": queryset, "comunas": comunas_santa_elena, "con_guia": "False",})

@login_required(login_url='login')
def mutable_table_with_guide(request):
	'''
	Method that calls another method that renders the table with the data, passing it the argument 
	to tell it to show only the	orders that have a dispatch order
	Page: mutable_table_show
	'''
	con_guia = "True"
	return mutable_table(request, con_guia)

@login_required(login_url='login')
def mutable_table_no_guide(request):
	'''
	Method that calls another method that renders the table with the data, passing it the argument 
	to tell it to show only the	orders that don't have a dispatch order
	Page: mutable_table_not_show
	'''
	con_guia = "False"
	return mutable_table(request, con_guia)

def mutable_table(request, con_guia):
	'''
	Renders the table with all the current data present in the database
	'''
	
	# If there's a POST request, it means user is trying to submit data into the database from the table
	if request.method == "POST":
		data = request.POST
		# POST request for changing the state of an order from the selection list on the table
		if (data['type'] == 'estado'):
			Ordenes.objects.filter(nvv=data['nvv']).update(estado=data['option'])
		# POST request for submitting the order as dispatched and retrieving its guide number from Random ERP database
		elif (data['type'] == 'numero_guia'):
			nvv = data['nvv']
			listo = 1-int(data['listo'])
			Ordenes.objects.filter(nvv=nvv).update(listo=listo)
			bool_n_guia = change_numero_guia(nvv, listo)
			# If there's no guide number, return garbage so it detects an error and prompts the user about it
			if (not bool_n_guia):
				return 'error'
		elif (data['type'] == 'rango_horario'):
			Ordenes.objects.filter(nvv=data['nvv']).update(rango_horario_final=data['option'])
		elif (data['type'] == 'estado_pedido_para_vendedor'):
			Ordenes.objects.filter(nvv=data['nvv']).update(estado_pedido_para_vendedor=data['option'])
		elif (data['type'] == 'fecha_despacho'):
			Ordenes.objects.filter(nvv=data['nvv']).update(fecha_despacho_final=data['date'])
		elif (data['type'] == 'observaciones_pedido'):
			Ordenes.objects.filter(nvv=data['nvv']).update(observacion_despacho=data['observaciones'])
	
	queryset = Ordenes.objects.all() # Get the data from the database
	
	groups = list(request.user.groups.values_list('name', flat= True)) # Get user permissions to pass it to the template so it knows what to show
	permissions = 'Básico'
	if (len(groups) > 0):
		permissions = groups[0]
	# TEMPORARY, JUST FOR DEBUGGING WHEN SUPERUSER IS LOGGED IN TO HAVE ALL PERMISSIONS
	if request.user.is_superuser:
		permissions = 'Despacho'
	return render(request, "AppMejoraDespacho/mutable_table.html",{"permissions": permissions, "queryset": queryset, "comunas": comunas_santa_elena, "con_guia": con_guia,})

def change_numero_guia(nvv, listo):
	'''
	Method for changing state of the order listo = not listo (ready to not ready)
	'''
	if not listo:
		# Change to not ready and return True so it knows it was succesful
		Ordenes.objects.filter(nvv=nvv).update(numero_guia='')
		return True
	else:
		# Retrieve the guide number from Random ERP database
		cursor = connections['dimaco'].cursor()
		cursor.execute(query_get_dispatch_guide, [nvv])
		datos = dictfetchall(cursor)
		if datos:
			# If there is, change it on this database and return True so it knows it was succesful
			n_guia = datos[0]['TIDO']+' Número '+ datos[0]['NUDO']
			Ordenes.objects.filter(nvv=nvv).update(numero_guia=n_guia)
			return True
		else:
			# If there isn't, change to not ready on this database and return False so it knows it wasn't succesful
			Ordenes.objects.filter(nvv=nvv).update(listo=0)
			return False

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def load_comunas(request):
	'''
	Method for loading the corresponding communes depending on the region selected
	on the form
	'''
	region = request.GET.get('region')
	com = comunas_todas[int(region)]
	return render(request, 'AppMejoraDespacho/comuna_dropdown_list_options.html', {'comunas': com})