from django.urls import path
from Pruebas import views
from Usuarios.views import login

urlpatterns = [
    path('', views.inicioPa, name="inicio"), 
    path('reminiscencia-1/', views.rmsc1, name="reminiscencia-1"),
    path('guardar/', views.saveAnswer, name="guardarRespuestas"),
    path('finishR/<clave>', views.setCalif, name = "terminarRem"),
    path('moca-1/', views.moca1, name="moca-1"),
    path('moca-2/', views.moca2, name="moca-2"),
    path('moca-3/', views.moca3, name="moca-3"),
    path('moca-4/', views.moca4, name="moca-4"),
    path('editarP/', views.editP, name="editarP"),
    path('../login', login, name="cerrarSesion"),
]