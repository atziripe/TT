from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Cuidador import views
from Usuario.views import login

urlpatterns = [
<<<<<<< HEAD
    path('<token>', views.inicioC, name='inicio'),
    path('cveAcceso/<token>/<treatment>', views.cveAcceso, name='CveC'),
    path('GetcveAcceso/<token>/<treatment>', views.getcveAcceso, name='GetCveC'),
    path('editarC/', views.editC, name="editarC"),
    path('ingresar-datos/<token>', views.ingresarDatos, name='ingresar'),
=======
    path('', views.inicioC, name='inicio'),
    path('cveAcceso/', views.cveAcceso, name='Cve'),
    path('GetcveAcceso/', views.getcveAcceso, name='GetCve'),
    path('editProfile/<token>/<tipo>/<name>', views.editC, name="editarC"),
    path('datosC/', views.ingrDatosC, name='datosC'),
    path('ingresar-datos/', views.ingresarDatos, name="ingresar"),
    path('../login', login, name="cerrarSesion"),
>>>>>>> 9fe2d3e5450a9a139074dff99e5cd21a11a99f1d
]

urlpatterns = format_suffix_patterns(urlpatterns)