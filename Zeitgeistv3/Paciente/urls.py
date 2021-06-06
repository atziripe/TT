from django.urls import path
from . import views
from Usuario.views import login

urlpatterns = [
    path('', views.inicioPa, name="inicioP"), 
    path('reminiscencia/<token>/<tipo>', views.rmsc1, name="reminiscencia-1"),
    path('guardar/', views.saveAnswer, name="guardarRespuestas"),
    path('finishR/<clave>/<token>/<tipo>', views.setCalif, name = "terminarRem"),
    path('editProfile/<token>/<tipo>/<name>', views.editP, name="editarP"),
    path('moca/<token>/<tipo>', views.moca, name="moca"),
    path('moca1/', views.moca1, name="moca-1"),
    path('moca2-3/', views.moca2_3, name="moca-2y3"),
    path('moca4/', views.moca4, name="moca-4"),
    path('moca5/', views.moca5, name="moca-5"),
    path('moca6/', views.moca6, name="moca-6"),
    path('moca7/', views.moca7, name="moca-7"),
    path('moca8/', views.moca8, name="moca-8"),
    path('moca9/', views.moca9, name="moca-9"),
    path('moca10/', views.moca10, name="moca-10"),
    path('moca11/', views.moca11, name="moca-11"),
    path('moca12/', views.moca12, name="moca-12"),
    path('moca13/', views.moca13, name="moca-13"),
    path('moca14/', views.moca14, name="moca-14"),
    path('mocaconfirm/<token>/<tipo>', views.finalizarmoca, name='final-moca'),
    path('sopa-de-letras/<token>/<tipo>', views.entCog, name="entCog"),
    path('entrenamientocogn/<token>/<tipo>', views.enterEntCogn, name='passEntCogn'),
    path('reportes/<token>/<tipo>', views.reportes, name='Reportes'),
    path('../login', login, name="cerrarSesion"),
]