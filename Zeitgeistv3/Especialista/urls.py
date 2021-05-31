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
    path('reportes/<token>/<tipo>', views.reportes, name="reportes"),
    path('calificarmoca/<cve>/<token>/<tipo>', views.califmoca, name="calificar-moca"),
    path('terminarmoca/<token>/<tipo>', views.modalfinishMoca, name="finishCalifMoca"),
    path('moca/<token>/<tipo>', views.moca, name="creaPDF"),
    path('moca-grafica/<token>/<tipo>', views.graphic, name="grafica"),    
]
