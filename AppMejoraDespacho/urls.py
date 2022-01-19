from django.urls import path, include
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),

    path('', views.inicio, name="inicio"),
    path('inicio', views.inicio, name="inicio"),
    path('form', views.ingresar, name='formulario'),
    path('confirm_nvv', views.confirm_nvv, name='confirm_nvv'),
    path('delete_nvv', views.delete_nvv, name='delete_nvv'),
    path('confirm_delete_nvv', views.confirm_delete_nvv, name='confirm_delete_nvv'),
    path('tabla_modificable', views.tabla_modificable_sin_guia, name='tabla_modificable'),
    path('tabla_modificable_con_guia', views.tabla_modificable_con_guia, name='tabla_modificable_mostrar'),
    
    path('ajax/load-comunas/', views.load_comunas, name='ajax_load_comunas'),

    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
]