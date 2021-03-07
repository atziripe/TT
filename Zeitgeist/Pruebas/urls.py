from django.urls import path
from Pruebas import views

urlpatterns = [
    path('', views.inicioPa, name="inicioP"), 
    path('reminiscencia-1/', views.rmsc1, name="reminiscencia-1"),
    path('reminiscencia-2/', views.rmsc2, name="reminiscencia-2"),
    path('reminiscencia-3/', views.rmsc3, name="reminiscencia-3"),
    path('editarP/', views.editP, name="editarP"),
]