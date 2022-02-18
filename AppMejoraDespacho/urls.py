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
    path('table_with_guide', views.table_with_guide, name='table_with_guide'),
    path('mutable_table', views.mutable_table_no_guide, name='mutable_table'),
    path('mutable_table_with_guide', views.mutable_table_with_guide, name='mutable_tabla_modificable_with_guide'),

    path('ajax/load-comunas/', views.load_comunas, name='ajax_load_comunas'),

    path('login', views.loginPage, name='login'),
    path('register_new', views.registerPage, name='register_new'),
    path('confirm_user', views.confirm_user, name='confirm_user'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('password_reset_done', views.password_reset_done, name='password_reset_done'),
    path('new_password/', views.create_new_password, name='new_password'),
    path('new_password/login', views.go_back_to_login, name='new_password/login'),
    path('create_new_password_success', views.create_new_password_success, name='create_new_password_success'),
    path('logout', views.logoutUser, name='logout'),
]