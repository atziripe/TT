from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Cuidador import views

urlpatterns = [
    path('', views.inicioC),
    path('cveAcceso/',views.cveAcceso, name="Cve"),
    path('getcveAcceso/',views.getcveAcceso, name="GetCve"),
    path('cuidador/', views.CuidadorList.as_view()),
    path('cuidador/<pk>/', views.CuidadorDetail.as_view()),
    path('editarC/', views.editC),
    path('datosC/', views.ingrDatosC, name="datosRem"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)