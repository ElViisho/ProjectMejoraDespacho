from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from AppMejoraDespacho.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connections

from AppMejoraDespacho.form import ingresoForm, deleteForm, editFileForm, CreateUserForm
import datetime
from django.db import connections

from ProjectMejoraDespacho.settings import MEDIA_ROOT

from .choices import comunas_metropolitana, comunas_biobio, comunas_todas, regiones
from .queries import *
from django.core.files.storage import FileSystemStorage
import os 

from django.utils.translation import activate

from .password_reset_token import *
from django.core.mail import send_mail
import smtplib

def loginPage(request):
	'''
	Renders the login page
	Whenever a user is not logged in and tries to go to other directions, 
	it goes back to here inmediately
	Page: login
	'''
	activate('es')
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

		
		return render(request, "AppMejoraDespacho/user_authentication/login.html", context)

def logoutUser(request):
	'''
	Method that handles the logging out of the app
	It redirects to the login page afterwards
	Page: logout
	'''
	activate('es')
	logout(request)
	return redirect('login')

def registerPage(request):
	'''
	Method that handles the regisration of a new user
	It redirects to the main page afterwards
	Page: register_new
	'''
	activate('es')
	if request.user.is_authenticated:
		return redirect('main')

	form = CreateUserForm()

	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('confirm_user')

	return render(request, 'AppMejoraDespacho/user_authentication/register_new.html', {'form':form})

def confirm_user(request):
	'''
	Method to show the succesful creating of a new user
	'''
	activate('es')
	if request.user.is_authenticated:
		return redirect('main')
	return render(request, "AppMejoraDespacho/confirmation_pages/confirm_user.html")

def password_reset(request):
	'''
	Method that shows the page for resetting a user password
	'''
	activate('es')
	if request.user.is_authenticated:
		return redirect('main')

	context = {}
	if request.method == "POST":
		mail = request.POST.get('mail')
		try:
			User.objects.get(username=mail)

			token = encoded_reset_token(mail)
			url = request.get_host()+'/new_password/?id='+token

			send_mail(
				'Cambio contraseña App despacho Dimaco',
				'''Se ha generado este mail porque se hizo una solicitud de cambio de contraseña. Para iniciar el proceso anda al siguiente link\n{} \n
En caso de que no hayas hecho esta solicitud, simplemente ignora este mensaje'''.format(url),
				None,
				[mail],
				fail_silently=False,
			)
			return redirect('password_reset_done')
		except smtplib.SMTPException:
			context = {"error":"Error al intentar mandar mail. Por favor reintentar"}
		except User.DoesNotExist:
			context = {"error":"No existe usuario asociado a mail ingresado."}
			
	return render(request, "AppMejoraDespacho/user_authentication/password_reset.html", context)
def password_reset_done(request):
	'''
	Method that shows the page for correct sending the password reset request
	'''
	activate('es')
	if request.user.is_authenticated:
		return redirect('main')
	
	return render(request, "AppMejoraDespacho/user_authentication/password_reset_done.html")
def create_new_password(request):
	'''
	Method that shows the page for creating a new password, but checks if token is expired
	to know if it's valid to change the password
	'''
	activate('es')
	if request.user.is_authenticated:
		return redirect('main')

	token = request.GET.get('id')
	mail = decode_reset_token(token)
	try:
		user = User.objects.get(username__exact=mail)
		if request.method == 'POST':
			password = request.POST.get('password')
			if (password != request.POST.get('password2')):
				return render(request, "AppMejoraDespacho/user_authentication/create_new_password.html", {'error': 'Contraseñas no son iguales.'})
			if len(password) < 8:
				return render(request, "AppMejoraDespacho/user_authentication/create_new_password.html", {'error': 'Contraseña debe tener al menos 8 caractéres'})
			first_isalpha = password[0].isalpha()
			if all(c.isalpha() == first_isalpha for c in password):
				return render(request, "AppMejoraDespacho/user_authentication/create_new_password.html", {'error': 'Contraseña debe tener al menos una letra y un dígito o símbolo'})

			user.set_password(password)
			user.save()
			return redirect('create_new_password_success')
	except:
		return render(request, "AppMejoraDespacho/user_authentication/create_new_password_fail.html")

	return render(request, "AppMejoraDespacho/user_authentication/create_new_password.html")
def create_new_password_success(request):
	'''
	Method to show the succesful changing the password
	'''
	activate('es')
	if request.user.is_authenticated:
		return redirect('main')
	
	return render(request, "AppMejoraDespacho/user_authentication/create_new_password_success.html")
def go_back_to_login(request):
	return redirect('login')



@login_required(login_url='login')
def main(request):
	'''
	Renders the base page of the app
	Page: main
	'''
	activate('es')
	# Get user groups to know which template and buttons to show
	# And redirect or show errors in case it doesn't have permissions
	groups = list(request.user.groups.values_list('name', flat= True))
	sucursal = request.GET.get('sucursal')

	cookie = request.COOKIES.get('cookie_sucursal')
	if sucursal is None and cookie is not None:
		sucursal = cookie

	context = get_sucursales(groups, sucursal)
	if not(context):
		return render(request, "AppMejoraDespacho/error.html")
	elif (context == 'sin_sede'):
		return render(request, "AppMejoraDespacho/sin_sede.html")

	sucursal = context['sucursal']

	if (request.user.is_superuser):
		template = "AppMejoraDespacho/main.html"
	elif ('Despacho' in groups):
		template = "AppMejoraDespacho/main_despacho.html"
	elif ('Eliminar' in groups):
		template = "AppMejoraDespacho/main_eliminar.html"
	else:
		template = "AppMejoraDespacho/main_basico.html"

	return response_with_cookie_sucursal(request, template, context, sucursal)

@login_required(login_url='login')
def submit_nvv_form(request):
	'''
	Renders the form for submitting a new order
	Page: submit_nvv_form
	'''
	activate('es')
	# Get user groups to know which template and buttons to show
	# And redirect or show errors in case it doesn't have permissions
	groups = list(request.user.groups.values_list('name', flat= True))
	sucursal = request.GET.get('sucursal')
	n_sucursal = sucursal
	
	if (not request.user.is_superuser and 'Despacho' in groups):
		return redirect("/?sucursal="+n_sucursal)

	cookie = request.COOKIES.get('cookie_sucursal')
	if sucursal is None and cookie is not None:
		sucursal = cookie

	context = get_sucursales(groups, sucursal)
	if not(context):
		return render(request, "AppMejoraDespacho/error.html")
	elif (context == 'sin_sede'):
		return render(request, "AppMejoraDespacho/sin_sede.html")

	sucursal = context['sucursal']
	n_sucursal = sucursal

	if (sucursal == '0'):
		sucursal = 'Colina'
	elif (sucursal == '1'):
		sucursal = 'Concepcion'
	elif (sucursal == '2'):
		sucursal = 'Santa Elena'

	if request.method == 'GET':
		# Get form withut data and pass it to the renderer
		formulario = ingresoForm(sucursal=sucursal)
		for field in formulario:
			field.field.widget.attrs.update({"class": "form-control"})
		context['formulario'] = formulario
		return response_with_cookie_sucursal(request, "AppMejoraDespacho/forms/submit_nvv_form.html", context, n_sucursal)
	if request.method == "POST":
		# Get the data from the post into the form and validate it
		data_obtenida = ingresoForm(request.POST or None, request.FILES or None, sucursal=sucursal)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			nvv = cleaned_data['nvv']

			comunas = comunas_todas
			if (cleaned_data['tipo_despacho'] == "1"):
				tipo_despacho = cleaned_data['despacho_externo'] + '\\' + cleaned_data['direccion_despacho_externo']
				comuna = comunas[int(cleaned_data['region'])][int(cleaned_data['comuna'])][1] + ', ' + regiones[int(cleaned_data['region'])][1] 
			elif sucursal != 'Concepcion':
				tipo_despacho = 'DIMACO'
				comuna = comunas[0][int(cleaned_data['comuna'])][1]
			else:
				tipo_despacho = 'DIMACO'
				comuna = comunas[int(cleaned_data['region'])][int(cleaned_data['comuna'])][1] + ', ' + regiones[int(cleaned_data['region'])][1]
                
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
				nombre_asistente = request.user.email,
				valor_neto_documento = datos_maeedo[0]["VANEDO"],
			)		
			return redirect("/confirm_nvv?sucursal="+n_sucursal)
		# If data not valid, rerender the page and don't lose the data that was already there
		context['formulario'] = data_obtenida
		return response_with_cookie_sucursal(request, "AppMejoraDespacho/forms/submit_nvv_form.html", context, n_sucursal)

@login_required(login_url='login')
def confirm_nvv(request):
	'''
	Renders the page that confirms the succesful submitting of a new order
	Page: confirm_nvv
	'''
	activate('es')
	return render(request, "AppMejoraDespacho/confirmation_pages/confirm_nvv.html")

@login_required(login_url='login')
def delete_nvv(request):
	'''
	Renders the form for deleting an order from the database
	Page: delete_nvv
	'''
	activate('es')
	# Get user groups to know which template and buttons to show
	# And redirect or show errors in case it doesn't have permissions
	groups = list(request.user.groups.values_list('name', flat= True))
	sucursal = request.GET.get('sucursal')
	n_sucursal = sucursal

	if (not request.user.is_superuser and not ('Eliminar' in groups) ):
		return redirect("/?sucursal="+n_sucursal)

	cookie = request.COOKIES.get('cookie_sucursal')
	if sucursal is None and cookie is not None:
		sucursal = cookie

	context = get_sucursales(groups, sucursal)
	if not(context):
		return render(request, "AppMejoraDespacho/error.html")
	elif (context == 'sin_sede'):
		return render(request, "AppMejoraDespacho/sin_sede.html")

	sucursal = context['sucursal']
	n_sucursal = sucursal

	if (sucursal == '0'):
		sucursal = 'COL'
	elif (sucursal == '1'):
		sucursal = 'CON'
	elif (sucursal == '2'):
		sucursal = 'V'
	
	if request.method == 'GET':
		formulario = deleteForm(sucursal=sucursal)
		for field in formulario:
			field.field.widget.attrs.update({"class": "form-control"})
		context['formulario'] = formulario
		return response_with_cookie_sucursal(request, "AppMejoraDespacho/forms/delete_nvv.html", context, n_sucursal)
	if request.method == "POST":
		data_obtenida = deleteForm(request.POST or None, sucursal=sucursal)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			Ordenes.objects.filter(nvv=cleaned_data['nvv']).delete()
			return redirect("/confirm_delete_nvv?sucursal="+n_sucursal)
		return response_with_cookie_sucursal(request, "AppMejoraDespacho/forms/delete_nvv.html", context, n_sucursal)

@login_required(login_url='login')
def confirm_delete_nvv(request):
	'''
	Renders the page that confirms the succesful deleting of an order
	Page: confirm_delete_nvv
	'''
	activate('es')
	return render(request, "AppMejoraDespacho/confirmation_pages/confirm_delete_nvv.html")

@login_required(login_url='login')
def table_with_guide(request):
	'''
	Method that calls another method that renders the table with the data, passing it the argument 
	to tell it to show only the	orders that have a dispatch order
	Page: table_show
	'''
	activate('es')
	con_guia = "True"
	return table(request, con_guia)
@login_required(login_url='login')
def table_no_guide(request):
	'''
	Method that calls another method that renders the table with the data, passing it the argument 
	to tell it to show only the	orders that don't have a dispatch order
	Page: table_not_show
	'''
	activate('es')
	con_guia = "False"
	return table(request, con_guia)
def table(request, con_guia):
	'''
	Renders the table with all the current data present in the database
	'''	
	activate('es')
	# Get user groups to know which template and buttons to show
	# And redirect or show errors in case it doesn't have permissions
	groups = list(request.user.groups.values_list('name', flat= True))
	sucursal = request.GET.get('sucursal')
	
	if (not request.user.is_superuser and 'Despacho' in groups):
		return redirect("/?sucursal="+sucursal)
	data_obtenida = editFileForm()

	cookie = request.COOKIES.get('cookie_sucursal')
	if sucursal is None and cookie is not None:
		sucursal = cookie

	context = get_sucursales(groups, sucursal)
	if not(context):
		return render(request, "AppMejoraDespacho/error.html")
	elif (context == 'sin_sede'):
		return render(request, "AppMejoraDespacho/sin_sede.html")

	sucursal = context['sucursal']
	n_sucursal = sucursal

	# Get depending on office
	if (sucursal == '0'):
		sucursal = 'COL'
		context["comunas"] = comunas_metropolitana
	elif (sucursal == '1'):
		sucursal = 'CON'
		context["comunas"] = comunas_biobio
	elif (sucursal == '2'):
		sucursal = 'V'
		context["comunas"] = comunas_metropolitana
	
	if (request.method == "POST"):
		data_obtenida = editFileForm(request.POST or None, request.FILES or None)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			nvv = cleaned_data["nvv_for_submit"]
			file = cleaned_data["nuevo_comprobante_pago"]

			obj = Ordenes.objects.filter(nvv=nvv)
			prev_file = os.path.join(MEDIA_ROOT, str(obj[0].comprobante_pago))
			if (prev_file != "None" and os.path.exists(prev_file)):
				os.remove(prev_file)

			now = datetime.datetime.now()
			fs = FileSystemStorage(os.path.join(MEDIA_ROOT,'comprobantes_de_pago', now.strftime("%Y/%m/%d/")))
			filename = fs.save(file.name, file)
			obj.update(comprobante_pago=os.path.join('comprobantes_de_pago/', now.strftime("%Y/%m/%d/"), filename))

	queryset = Ordenes.objects.filter(nvv__startswith=sucursal) # Get the data from the database
	
	permissions = 'Básico'
	if (request.user.is_superuser or 'Eliminar' in groups):
		permissions = "Eliminar"
	context["permissions"] = permissions
	context["queryset"] = queryset
	
	context["con_guia"] = con_guia
	context["formulario"] = data_obtenida
	return response_with_cookie_sucursal(request, "AppMejoraDespacho/tables/table.html", context, n_sucursal)



@login_required(login_url='login')
def mutable_table_with_guide(request):
	'''
	Method that calls another method that renders the table with the data, passing it the argument 
	to tell it to show only the	orders that have a dispatch order
	Page: mutable_table_show
	'''
	activate('es')
	con_guia = "True"
	return mutable_table(request, con_guia)
@login_required(login_url='login')
def mutable_table_no_guide(request):
	'''
	Method that calls another method that renders the table with the data, passing it the argument 
	to tell it to show only the	orders that don't have a dispatch order
	Page: mutable_table_not_show
	'''
	activate('es')
	con_guia = "False"
	return mutable_table(request, con_guia)
def mutable_table(request, con_guia):
	'''
	Renders the table with all the current data present in the database,
	whose some data may be changed
	'''
	activate('es')
	# Get user groups to know which template and buttons to show
	# And redirect or show errors in case it doesn't have permissions
	groups = list(request.user.groups.values_list('name', flat= True))
	sucursal = request.GET.get('sucursal')

	if (not request.user.is_superuser and not ('Despacho' in groups)):
		return redirect("/?sucursal="+sucursal)

	data_obtenida = editFileForm()

	cookie = request.COOKIES.get('cookie_sucursal')
	if sucursal is None and cookie is not None:
		sucursal = cookie

	context = get_sucursales(groups, sucursal)
	if not(context):
		return render(request, "AppMejoraDespacho/error.html")
	elif (context == 'sin_sede'):
		return render(request, "AppMejoraDespacho/sin_sede.html")

	sucursal = context['sucursal']
	n_sucursal = sucursal

	# Get depending on office
	if (sucursal == '0'):
		sucursal = 'COL'
		context["comunas"] = comunas_metropolitana
	elif (sucursal == '1'):
		sucursal = 'CON'
		context["comunas"] = comunas_biobio
	elif (sucursal == '2'):
		sucursal = 'V'
		context["comunas"] = comunas_metropolitana
	
	# If there's a POST request, it means user is trying to submit data into the database from the table
	if request.method == "POST":
		data_obtenida = editFileForm(request.POST or None, request.FILES or None)
		if data_obtenida.is_valid():
			cleaned_data = data_obtenida.cleaned_data
			nvv = cleaned_data["nvv_for_submit"]
			file = cleaned_data["nuevo_comprobante_pago"]

			obj = Ordenes.objects.filter(nvv=nvv)
			prev_file = os.path.join(MEDIA_ROOT, str(obj[0].documento_salida))
			if (prev_file != "None" and os.path.exists(prev_file)):
				os.remove(prev_file)

			now = datetime.datetime.now()
			fs = FileSystemStorage(os.path.join(MEDIA_ROOT,'voucher_de_despacho', now.strftime("%Y/%m/%d/")))
			filename = fs.save(file.name, file)
			obj.update(documento_salida=os.path.join('voucher_de_despacho/', now.strftime("%Y/%m/%d/"), filename))
		else:
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
					response = JsonResponse({"error": "there was an error"})
					response.status_code = 403 # To announce that the user isn't allowed to publish
					return response
			# POST request for submitting a new hour range for dispatch of the order
			elif (data['type'] == 'rango_horario'):
				Ordenes.objects.filter(nvv=data['nvv']).update(rango_horario_final=data['option'])
			# POST request for changing the state of the order for the seller (different list than the other)
			elif (data['type'] == 'estado_pedido_para_vendedor'):
				Ordenes.objects.filter(nvv=data['nvv']).update(estado_pedido_para_vendedor=data['option'])
			# POST request for submitting a new dispatch date
			elif (data['type'] == 'fecha_despacho'):
				Ordenes.objects.filter(nvv=data['nvv']).update(fecha_despacho_final=data['date'])
			# POST request for submitting new observations that may be pertinent
			elif (data['type'] == 'observaciones_pedido'):
				Ordenes.objects.filter(nvv=data['nvv']).update(observacion_despacho=data['observaciones'])
			
	
	# Get depending on office
	queryset = Ordenes.objects.filter(nvv__startswith=sucursal) # Get the data from the database
	
	groups = list(request.user.groups.values_list('name', flat= True)) # Get user permissions to pass it to the template so it knows what to show
	permissions = 'Básico'
	if (request.user.is_superuser or 'Despacho' in groups):
		permissions = "Despacho"
	context["permissions"] = permissions
	context["queryset"] = queryset
	
	context["con_guia"] = con_guia
	context["formulario"] = data_obtenida
	return response_with_cookie_sucursal(request, "AppMejoraDespacho/tables/mutable_table.html", context, n_sucursal)

def change_numero_guia(nvv, listo):
	'''
	Method for changing state of the order listo = not listo (ready to not ready)
	'''
	activate('es')
	if not listo:
		# Change to not ready and return True so it knows it was succesful
		Ordenes.objects.filter(nvv=nvv).update(numero_guia='')
		return True
	else:
		# Retrieve the guide number from Random ERP database
		cursor = connections['dimaco'].cursor()
		cursor.execute(query_get_dispatch_guide.format(nvv))
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
	return render(request, 'AppMejoraDespacho/utilities/comuna_dropdown_list_options.html', {'comunas': com})

def get_sucursales(groups, sucursal):
	s = sucursal
	colina = '0'
	concepcion = '0'
	santa_elena = '0'
	sedes_usuario = []
	if ('Colina' in groups):
		colina = '1'
		sedes_usuario += '0'
	if ('Concepcion' in groups):
		concepcion = '1'
		sedes_usuario += '1'
	if ('Santa Elena' in groups):
		santa_elena = '1'
		sedes_usuario += '2'

	if (s is None):
		try:
			s = sedes_usuario[0]
		except: 
			return 'sin_sede'

	if not (s in ['0', '1', '2']) or not(s in sedes_usuario):
		return False
		
	return {'sucursal': s, 'colina': colina, 'concepcion': concepcion, 'santa_elena': santa_elena,}

def response_with_cookie_sucursal(request, template, context, sucursal):
	'''
	Returns a http response with the cookie of the last sucursal the user
	used, so it is restores the next session
	'''
	response = render(request, template, context)
	response.set_cookie('cookie_sucursal', sucursal, max_age=2678400)
	return response

def handler404(request, exception):
	'''
	Method for handling the 404 error
	'''
	return render(request, '404.html')

def handler500(request):
	'''
	Method for handling the 500 error
	'''
	return render(request, '500.html')