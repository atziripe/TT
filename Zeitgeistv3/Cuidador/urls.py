from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Cuidador import views

urlpatterns = [
    path('<token>', views.inicioC, name='inicio'),
    path('cveAcceso/<token>', views.cveAcceso, name='CveC'),
    path('GetcveAcceso/<token>', views.getcveAcceso, name='GetCveC'),
    path('editarC/', views.editC, name="editarC"),
    path('ingresar-datos/<token>', views.ingresarDatos, name='ingresar'),
]

urlpatterns = format_suffix_patterns(urlpatterns)