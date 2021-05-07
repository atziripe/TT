from django.urls import path
from . import views
from Usuario.views import login

urlpatterns = [
    path('', views.inicioPa, name="inicioP"), 
    path('reminiscencia/<token>', views.rmsc1, name="reminiscencia-1"),
    path('guardar/', views.saveAnswer, name="guardarRespuestas"),
    path('finishR/<clave>/<token>', views.setCalif, name = "terminarRem"),
    path('editProfile/<token>', views.editP, name="editarP"),
    path('moca/<token>', views.moca, name="moca"),
    path('moca1/', views.moca1, name="moca-1"),
    path('moca4/', views.moca4, name="moca-4"),
    path('moca9/', views.moca9, name="moca-9"),
    path('moca12/', views.moca12, name="moca-12"),
    path('moca13/', views.moca13, name="moca-13"),
    path('moca14/', views.moca14, name="moca-14"),
    path('../login', login, name="cerrarSesion"),
]