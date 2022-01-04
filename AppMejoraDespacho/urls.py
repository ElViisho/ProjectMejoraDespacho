from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('inicio', views.inicio, name="inicio"),
    path('form', views.ingresar, name='formulario'),
    path('confirm_nvv', views.confirm_nvv, name='confirm_nvv'),
    path('tabla', views.tabla, name='tabla'),
]