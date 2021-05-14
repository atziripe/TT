from django.urls import path
from . import views
from Usuario.views import login

urlpatterns = [
    path('', views.inicioPa, name="inicioP"), 
    path('reminiscencia/<token>', views.rmsc1, name="reminiscencia-1"),
    path('guardar/', views.saveAnswer, name="guardarRespuestas"),
<<<<<<< HEAD
    path('finishR/<clave>/<token>', views.setCalif, name = "terminarRem"),
    path('editProfile/<token>', views.editP, name="editarP"),
=======
    path('finishR/<clave>', views.setCalif, name = "terminarRem"),
    path('editProfile/<token>/<tipo>/<name>', views.editP, name="editarP"),
>>>>>>> 9fe2d3e5450a9a139074dff99e5cd21a11a99f1d
    path('moca/<token>', views.moca, name="moca"),
    path('moca1/', views.moca1, name="moca-1"),
    path('moca4/', views.moca4, name="moca-4"),
    path('moca9/', views.moca9, name="moca-9"),
    path('moca12/', views.moca12, name="moca-12"),
    path('moca13/', views.moca13, name="moca-13"),
    path('moca14/', views.moca14, name="moca-14"),
    path('sopa-de-letras/<token>', views.entCog, name="entCog"),
    path('entrenamientocogn/<token>', views.enterEntCogn, name='passEntCogn'),
    path('../login', login, name="cerrarSesion"),
]