from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),

    path('', views.inicio, name="inicio"),
    path('inicio', views.inicio, name="inicio"),
    path('form', views.ingresar, name='formulario'),
    path('confirm_nvv', views.confirm_nvv, name='confirm_nvv'),
    path('modificar_nvv', views.modificar_nvv, name='modificar_nvv'),
    path('tabla', views.tabla, name='tabla'),
    path('pa', views.pa_probar, name='pa'),
    
    path('ajax/load-comunas/', views.load_comunas, name='ajax_load_comunas'),
]