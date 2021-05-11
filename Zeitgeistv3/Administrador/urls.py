from django.contrib import admin
from django.urls import path, include 
from . import views
from Usuario.views import login, regA


urlpatterns = [
    path('', views.inicioA, name="inicioA"),
    path('editProfile/<token>/<tipo>/<name>', views.editA, name="editarA"),
    path('../login/', login, name="cerrarSesion"),
    path('opcionesAdmin/<token>/<tipo>/<name>', views.modificarEliminarU, name="Modificar_EliminarU"),
    path('../registroA/<token>/<tipo>/<name>', regA, name="registrarA"),
    #path('eliminarPerfiles/<token>/<tipo>/<name>', views.eliminarPerfs, name="eliminarPerfs")
]
