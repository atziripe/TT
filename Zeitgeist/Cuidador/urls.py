from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Cuidador import views

urlpatterns = [
    path('', views.inicioC, name='inicio'),
    path('cuidador/', views.CuidadorList.as_view()),
    path('cuidador/<pk>/', views.CuidadorDetail.as_view()),
    path('editarC/', views.editC),
    path('datosC/', views.ingrDatosC, name='datosC'),
    path('ingresar-datos/', views.ingresarDatos, name="ingresar"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)