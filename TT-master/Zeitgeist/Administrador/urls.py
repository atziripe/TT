from django.contrib import admin
from django.urls import path, include 
from . import views
from Usuarios.views import login


urlpatterns = [
    path('', views.inicioA, name="inicio"),
    path('editarA/', views.editA, name="editarA"),
    path('../login/', login, name="cerrarSesion"),
    path('modificarRelaciones/', views.modificarRels, name="modificarRels"),
    path('eliminarPerfiles/', views.eliminarPerfs, name="eliminarPerfs")
]
