from django.urls import path
from Especialista import views

urlpatterns = [
    path('', views.inicioEsp, name="inicioE"), 
    path('cveAcceso/<token>', views.cveAcceso, name="Cve"), 
    #path('editarE/', views.editEsp, name="editarE"),
]
