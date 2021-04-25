from django.urls import path
from Especialista import views
from Usuarios.views import login

urlpatterns = [
    path('', views.inicioEsp, name="inicio"), 
    path('editarE/', views.editE, name="editarE"),
    path('../login', login, name="cerrarSesion"),
]
