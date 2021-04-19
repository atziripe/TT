from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.inicio, name="Index"),
    path('registroC/', views.regC, name="Cuidador"),
    path('registroE/', views.regE, name="Especialista"),
    path('registroP/', views.regP, name="Paciente"),
    path('registroA/', views.regA, name="Administrador"),
    path('recuperarPass/', views.recPasswd, name="Recuperar"),
    path('login/', views.login, name="Iniciar"),
   # path('cuidador/', include('Cuidador.urls'),name='inicioC'),
]
