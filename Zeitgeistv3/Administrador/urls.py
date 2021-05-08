from django.contrib import admin
from django.urls import path, include 
from . import views
from Usuario.views import login, regA


urlpatterns = [
    path('', views.inicioA, name="inicioA"),
    path('editProfile/<token>', views.editA, name="editarA"),
    path('../login/', login, name="cerrarSesion"),
    path('modificarRelaciones/', views.modificarRels, name="modificarRels"),
    path('../registroA/<token>', regA, name="registrarA")
]
