from django.urls import path
from Cuidador import views

urlpatterns = [
    path('', views.inicioC),
    path('editarC/', views.editC),
    path('datosC/', views.ingrDatosC),
]
