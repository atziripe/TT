from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Cuidador import views
from Usuario.views import login

urlpatterns = [
    path('<token>/<tipo>', views.inicioC, name='inicio'),
    path('cveAcceso/<token>/<treatment>/<tipo>', views.cveAcceso, name='CveC'),
    path('GetcveAcceso/<token>/<treatment>/<tipo>', views.getcveAcceso, name='GetCveC'),
    path('ingresar-datos/<token>/<tipo>', views.ingresarDatos, name='ingresar'),
    path('editProfile/<token>/<tipo>/<name>', views.editC, name="editarC"),
    path('../login', login, name="cerrarSesion"),
]

urlpatterns = format_suffix_patterns(urlpatterns)