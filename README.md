Este proyecto ya no se puede correr ya que está actualmente
configurado para correr en un windows server y además 
necesita acceso a una base de datos que está en una red 
privada de la empresa. Igual se deja el repositorio público 
para poder ver cosas de implementación. 

[<img src="static/images/logo.png">](https://dimacosac.cl)

# ProjectMejoraDespacho

### Aplicación web desarrollada en [Django](https://www.djangoproject.com/) para mejorar el proceso de despacho en [Dimaco](https://dimacosac.cl).
El objetivo principal es poder subir las órdenes de despacho con la menor cantidad de errores posibles para facilitar los procesos.

## Requerimientos y utilización
Para probar, utilizar y/o trabajar se debe tener instalado [Python](https://www.python.org/) junto a su instalador de paquetes pip. Luego, se deben instalar los requerimientos, corriendo el siguiente comando dentro de la carpeta del proyecto (idealmente con un [entorno virtual de python](https://docs.python.org/es/3/library/venv.html) activado dentro de esta carpeta):
```
pip install -r requeriments.txt
```
Luego hacer las migrations de los modelos de la aplicación:
```
python manage.py migrate
```
Y finalmente correr la aplicación:
```
python manage.py runserver
```
Luego, en un navegador ir a la dirección `http://127.0.0.1:8000/` debería aparecer la aplicación donde se puede navegar.

## Estructura proyecto
La estructura del proyecto es bastante estándar para una aplicación implementada en Django. Tiene los archivos base del proyecto en la carpeta ProjectMejoraDespacho y la aplicación AppMejoraDespacho donde está toda la lógica principal de la aplicación.

## AppMejoraDespacho
La única aplicación del proyecto por ahora. También sigue una estructura bien estándar de Django.

### models.py
En este archivo están los modelos que la aplicación utiliza. En este momento existe solo uno, ya que los id solo tienen un elemento para cada celda, por lo tanto no se necesita más complejidad. Este modelo, llamado Ordenes, guarda el número (único, por tanto también es llave primario) de una orden y le asocia todos los datos pertinenetes.

Los datos de cada orden son extraídos de la base de datos con la que ya trabaja la empresa, desarrollada por la ERP Random.

### form.py
Los formularios que hay en este archivo son solo dos, uno para ingresar órdenes a la base y otro para eliminarlas. Estos formularios tienen varios widgets para facilitar el ingreso de los datos y que sea menos propenso a que los usuarios cometan errores.

### views.py
Archivo donde se encuentra la lógica para desplegar cada una de las páginas de la aplicación. 

### choices.py
Archivo extra creado por el desarrollador de la aplicación, donde están los distintos arreglos de elecciones que se utilizan en ciertos elementos de la aplicación.

### queries.py
Archivo extra creado por el desarrollador de la aplicación, donde están las consultas que se hacen a la base de datos que desarrollo la ERP Random, para obtener los datos pertienentes.

### password_reset_token.py
Archivo extra creado por el desarrollador de la aplicación. Aquí están las funciones para codificar y decodificar los tokens aleatorios creados para el cambio de contraseña de un usario.

## Aplicaciones y plugins utilizados
Instalados con pip:  
- [Django](https://www.djangoproject.com/)  
- [asgiref](https://github.com/django/asgiref)  
- [pytz](https://pypi.org/project/pytz/)  
- [sqlparse](https://pypi.org/project/sqlparse/)  
- [mssql-django](https://docs.microsoft.com/en-us/samples/azure-samples/mssql-django-samples/mssql-django-samples/)  
- [django-file-resubmit](https://github.com/un1t/django-file-resubmit)  
- [python-magic-bin](https://pypi.org/project/python-magic-bin/)  
- [django-phonenumber-field](https://github.com/stefanfoulis/django-phonenumber-field)  
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)

Otros:
- [Bootstrap](https://getbootstrap.com/)
- [jQuery](https://jquery.com/)
- [Select2](https://select2.org/)
- [International Telephone Input](https://intl-tel-input.com/)
- [DataTables](https://datatables.net/)


## Créditos
Desarrollado por Vicente Videla [GitHub <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" style="height: 16px;">](https://github.com/ElViisho).  
Toda la propiedad de este proyecto pertenece a DIMACO SAC.
