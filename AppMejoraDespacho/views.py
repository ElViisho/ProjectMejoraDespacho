from django.shortcuts import render

def inicio(request):
	'''
	Funcion para mostrar el html inicio de la aplicacion con render
	Pagina: inicio
	'''
	return render(request, "AppMejoraDespacho/inicio.html")
