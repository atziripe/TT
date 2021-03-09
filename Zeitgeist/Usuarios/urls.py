from django.contrib import admin
from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.inicio, name="Index"),
    path('registroC/', views.regC, name="Cuidador"),
    path('registroP/', views.regP, name="Paciente"),
    path('recuperarPass/', views.recPasswd, name="Recuperar"),
    path('login/', views.login, name="Iniciar"),
]
