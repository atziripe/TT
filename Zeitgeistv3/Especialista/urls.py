from django.urls import path
from Especialista import views
from Usuario.views import login

urlpatterns = [
    path('', views.inicioEsp, name="inicioE"), 
    path('editProfile/<token>', views.editE, name="editarE"),
    path('cveAcceso/<token>', views.cveAcceso, name="Cve"), 
    path('../login', login, name="cerrarSesion"),
]
