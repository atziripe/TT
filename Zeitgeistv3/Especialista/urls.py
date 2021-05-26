from django.urls import path
from Especialista import views
from Usuario.views import login

urlpatterns = [
    path('', views.inicioEsp, name="inicioE"), 
    path('cveAcceso/<token>', views.cveAcceso, name="Cve"),
    path('reportes/', views.reportes, name="reportes"),
    path('moca/', views.moca, name="creaPDF"),
    path('moca-grafica/', views.graphic, name="grafica"),    
    #path('editarE/', views.editEsp, name="editarE"),
]
