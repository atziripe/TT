from django.urls import path
from Especialista import views

urlpatterns = [
    path('', views.inicioEsp, name="inicioE"), 
    #path('editarE/', views.editEsp, name="editarE"),
]
