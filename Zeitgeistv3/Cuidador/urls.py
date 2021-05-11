from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Cuidador import views
from Usuario.views import login

urlpatterns = [
    path('', views.inicioC, name='inicio'),
    path('cveAcceso/', views.cveAcceso, name='Cve'),
    path('GetcveAcceso/', views.getcveAcceso, name='GetCve'),
    path('editProfile/<token>/<tipo>/<name>', views.editC, name="editarC"),
    path('datosC/', views.ingrDatosC, name='datosC'),
    path('ingresar-datos/', views.ingresarDatos, name="ingresar"),
    path('../login', login, name="cerrarSesion"),
]

urlpatterns = format_suffix_patterns(urlpatterns)