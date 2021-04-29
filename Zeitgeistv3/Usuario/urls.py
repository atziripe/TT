from django.urls import path
from . import views
from . import apiviews
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
       path('', views.inicio, name="Index"),
       path('registroC/', views.regC, name="Cuidador"),
       path('registroE/', views.regE, name="Especialista"),
       path('registroP/', views.regP, name="Paciente"),
       path('registroA/', views.regA, name="Administrador"),
       path('recuperarPass/', views.recPasswd, name="Recuperar"),
        path('login/', views.login, name="Iniciar"),


       path('v1/createuser/', apiviews.UserCreate.as_view(), name='CrearUSuario'),
       path('v1/createpacient/', apiviews.PacienteCreate.as_view(), name='CrearPaciente'),
       path('v1/createspecialist/', apiviews.EspecialistCreate.as_view(), name='CrearEspecialista'),
       path('v1/createcare/', apiviews.CuidadorCreate.as_view(), name='CrearCuidador'),
       path('v1/createadmin/', apiviews.AdminCreate.as_view(), name='CrearAdmin'),
       path('v1/updategroup/<int:cat_pk>', apiviews.UpdateUserGroup.as_view(), name='Establecer grupo'),

       path('v1/listpacient/', apiviews.ListPaciente.as_view(), name='ListarPaciente'),
       path('v1/listspecialist/', apiviews.ListEspecialista.as_view(), name='ListarEspecialista'),
       path('v1/listcare/', apiviews.ListCuidador.as_view(), name='ListarCuidador'),
       path('v1/listusers/', apiviews.ListUsers.as_view(), name='ListarUsuarios'),

       path('v1/pacientsd/<int:pk>', apiviews.PacienteSelDel.as_view(), name='SDUPaciente'),
       path('v1/specialistsd/<int:pk>', apiviews.EspecialistaSelDel.as_view(), name='SDUEspecialista'),
       path('v1/caresd/<int:pk>', apiviews.CuidadorSelDel.as_view(), name='SDUCuidador'),
       path('v1/userd/<int:pk>', apiviews.UserSelDel.as_view(), name='DUser'),
       
       path('v1/Pacienteuser/<int:pk>/', apiviews.PacienteUser.as_view(), name='PacienteUser'),
       path('v1/Especialistauser/<int:pk>/', apiviews.EspecialistaUser.as_view(), name='EspecialistaUser'),
       path('v1/Cuidadoruser/<int:pk>/', apiviews.CuidadorUser.as_view(), name='CuidadorUser'),
       path('v1/Administradoruser/<int:pk>/', apiviews.AdministradorUser.as_view(), name='AdministradorUser'),

       path('v2/login/', apiviews.LoginView.as_view(), name="login"),

       path('v3/token/', csrf_exempt(apiviews.MyTokenObtainPairView.as_view()), name='token_obtain_pair'),
       path('v3/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



]
