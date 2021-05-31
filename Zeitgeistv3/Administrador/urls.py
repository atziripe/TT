from django.contrib import admin
from django.urls import path, include 
from Administrador import views
from Usuario.views import login, regA


urlpatterns = [
    path('<token>', views.inicioA, name="inicioA"),
    path('editProfile/<token>/<tipo>/<name>', views.editA, name="editarA"),
    path('../login/', login, name="cerrarSesion"),
    path('opcionesAdmin/<token>/<tipo>/<name>', views.modificarEliminarU, name="Modificar_EliminarU"),
    path('editarRelacionesP/<token>/<tipo>/<name>/<paciente>', views.editarRelacionesP, name="relacionesP"),
    path('eliminarUsuario/<token>/<tipo>/<name>/<e_usuario>/<e_username>', views.eliminarU, name="eliminarU"),
    path('../registroA/<token>/<tipo>/<name>', regA, name="registrarA"),
    #path('eliminarPerfiles/<token>/<tipo>/<name>', views.eliminarPerfs, name="eliminarPerfs")
]