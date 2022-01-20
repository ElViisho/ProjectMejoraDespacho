from django.urls import path, include
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),

    path('', views.main, name="main"),
    path('main', views.main, name="main"),
    path('submit_nvv_form', views.submit_nvv_form, name='submit_nvv_form'),
    path('confirm_nvv', views.confirm_nvv, name='confirm_nvv'),
    path('delete_nvv', views.delete_nvv, name='delete_nvv'),
    path('confirm_delete_nvv', views.confirm_delete_nvv, name='confirm_delete_nvv'),
    path('table', views.table_no_guide, name='table'),
    path('table_with_guide', views.table_with_guide, name='tabla_modificable_mostrar'),

    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
]