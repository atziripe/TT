from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Index.urls')),
    path('inicioPaciente/', include('Pruebas.urls'),name='inicioP'),
    #path('inicioC/', inicioC),
    #path('editarC/', editC),
    #path('registroC/', regC),
    #path('registroP/', regP),
    #path('recuperarPass/', recPasswd),
    #path('ingresarDatosC/', ingrDatosC),
]
