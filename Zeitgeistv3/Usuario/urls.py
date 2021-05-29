from django.urls import path, re_path
from . import views
from . import apiviews
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.inicio, name="Index"),
    path('registroC/', views.regC, name="Cuidador"),
    path('registroE/', views.regE, name="Especialista"),
    path('registroP/', views.regP, name="Paciente"),
    path('registroA/<token>/<tipo>/<name>', views.regA, name="Administrador"),
    path('chpwd/<iduser>/<token>/<tipo>/<name>', views.cambiarPasswd, name="CambiarPwd"),
    path('recuperarPass/', views.recPasswd, name="Recuperar"),
    path('resetpwdconfirm/', views.recPassConfirm, name='pwd_reset_confirm'),
    path('login/', views.login, name="Iniciar"),
    path('reset/password_reset', PasswordResetView.as_view(template_name='Usuarios/resetPwd/password_reset_form.html', email_template_name="Usuarios/resetPwd/password_reset_email.html"), name = 'password_reset'),
    path('reset/password_reset_done', PasswordResetDoneView.as_view(template_name='Usuarios/resetPwd/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='Usuarios/resetPwd/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('reset/done',PasswordResetCompleteView.as_view(template_name='Usuarios/resetPwd/password_reset_complete.html') , name = 'password_reset_complete'),




    path('v1/createuser/', apiviews.UserCreate.as_view(), name='CrearUSuario'),
    path('v1/createpacient/', apiviews.PacienteCreate.as_view(), name='CrearPaciente'),
    path('v1/createspecialist/', apiviews.EspecialistCreate.as_view(), name='CrearEspecialista'),
    path('v1/createcare/', apiviews.CuidadorCreate.as_view(), name='CrearCuidador'),
    path('v1/createadmin/', apiviews.AdminCreate.as_view(), name='CrearAdmin'),

    path('v1/listpacient/', apiviews.ListPaciente.as_view(), name='ListarPaciente'),
    path('v1/listspecialist/', apiviews.ListEspecialista.as_view(), name='ListarEspecialista'),
    path('v1/listcare/', apiviews.ListCuidador.as_view(), name='ListarCuidador'),
    path('v1/listadmins/', apiviews.ListAdministrador.as_view(), name='ListarAdministrador'),
    path('v1/listusers/', apiviews.ListUsers.as_view(), name='ListarUsuarios'),

    path('v1/pacientsd/<int:pk>', apiviews.PacienteSelDel.as_view(), name='SDUPaciente'),
    path('v1/specialistsd/<int:pk>', apiviews.EspecialistaSelDel.as_view(), name='SDUEspecialista'),
    path('v1/caresd/<int:pk>', apiviews.CuidadorSelDel.as_view(), name='SDUCuidador'),
    path('v1/userd/<int:pk>', apiviews.UserSelDel.as_view(), name='DUser'),
    path('v1/editarperfil/<int:pk>', apiviews.UpdateProfileView.as_view(), name='UpdateProfile'),
    path('v1/editarpaciente/<int:pk>', apiviews.UpdatePacientView.as_view(), name='UpdatePacient'),
    path('v1/editarespecialista/<int:pk>', apiviews.UpdateEspecialistaView.as_view(), name='UpdateEspecialista'),

    path('v1/Pacienteuser/<int:pk>/', apiviews.PacienteUser.as_view(), name='PacienteUser'),
    path('v1/Especialistauser/<int:pk>/', apiviews.EspecialistaUser.as_view(), name='EspecialistaUser'),
    path('v1/Cuidadoruser/<int:pk>/', apiviews.CuidadorUser.as_view(), name='CuidadorUser'),
    path('v1/Administradoruser/<int:pk>/', apiviews.AdministradorUser.as_view(), name='AdministradorUser'),
    path('v1/UserEmail/<pk>/', apiviews.UserperEmail.as_view(), name='SearchUserEmail'), #Endppoint para hacer la busqueda del usuario por su email para recuperar su contraseña

    path('v2/login/', apiviews.LoginView.as_view(), name="login"),

    path('v3/token/', csrf_exempt(apiviews.MyTokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('v3/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('v3/cambiarpwd/<int:pk>/', apiviews.ChangePasswordView.as_view(), name='auth_change_password'),

]
