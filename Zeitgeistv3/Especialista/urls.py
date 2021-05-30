from django.urls import path
from Especialista import views
from Usuario.views import login

urlpatterns = [
    path('<token>', views.inicioEsp, name="inicioE"), 
    path('editProfile/<token>/<tipo>/<name>', views.editE, name="editarE"),
    path('cveAcceso/<token>/<tipo>', views.cveAcceso, name="Cve"), 
    path('visualizarPacientes/<token>/<tipo>', views.verPacientes, name="verPacientes"),
    path('enviarMensajeC/<token>/<tipo>/<pacienteC>', views.mensajeCuidador, name="mensajeC"),
    path('../login', login, name="cerrarSesion"),
    path('reportes/<token>/', views.reportes, name="reportes"),
    path('terminarmoca/', views.modalfinishMoca, name="finishCalifMoca"),
    path('moca/', views.moca, name="creaPDF"),
    path('moca-grafica/', views.graphic, name="grafica"),    
    #path('editarE/', views.editEsp, name="editarE"),
]
