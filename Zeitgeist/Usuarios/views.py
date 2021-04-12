from django.http import HttpResponse
from django.shortcuts import render
from Usuarios.forms import FormLogin #API Forms
from Usuarios.forms import FormRegistroC #API Forms
from Usuarios.forms import FormRegistroP #API Forms
from Pruebas.models import Paciente
from Cuidador.models import Cuidador
from Especialista.models import Especialista
from Administrador.models import Administrador
from django_cryptography.fields import encrypt
import jwt, json


def inicio(request):
    return render(request, "Usuarios/index.html")

def regC(request):
    if request.method=="POST": 
        fregC = FormRegistroC(data=request.POST)
        if fregC.is_valid():
            nombre = fregC.cleaned_data['nombre']
            user = fregC.cleaned_data['nombreUsuario']
            email = fregC.cleaned_data['correo']
            pwd = fregC.cleaned_data['contrasena']
            pwd2 = fregC.cleaned_data['confirmacion_cont']

	    #Comparar contraseñas
	    #Mandar los datos capturados a la lista de pacientes
	#else:
	 #   print("Por favor introduzca los datos de manera correcta")
    else:
        fregC=FormRegistroC()
    return render(request, "Usuarios/registroCuidador.html", {"form": fregC})


def regP(request):
    if request.method=="POST":
        fregC = FormRegistroP(data=request.POST)
        if fregC.is_valid():
            nombre = fregP.cleaned_data['nombre']
            user = fregP.cleaned_data['nombreUsuario']
            email = fregP.cleaned_data['correo']
            pwd = fregP.cleaned_data['contrasena']
            pwd2 = fregP.cleaned_data['confirmacion_cont']
            sexo = fregP.cleaned_data['sexo']
            fNac = fregP.cleaned_data['fechaNac']
            escolaridad = fregP.cleaned_data['escolaridad']
            fDiag = fregP.cleaned_data['fechaDiag']

	    #Comparar contraseñas
	    #Mandar los datos capturados a la lista de pacientes
    else:
        fregP=FormRegistroP()
        print("Por favor introduzca los datos de manera correcta")
    return render(request, "Usuarios/registroPaciente.html", {"form": fregP})


def recPasswd(request):
    return render(request, "Usuarios/recuperarC.html")

def ObtenerTipo(user, pwd, tipo):
    if tipo == '1':
        res = Administrador.objects.filter(nomUsuario= user, contraseña = pwd)
    elif tipo == '2':
        res = Cuidador.objects.filter(nomUsuario= user, contraseña = pwd)
    elif tipo == '3':
        res = Especialista.objects.filter(nomUsuario= user, contraseña = pwd)
    else:
        res = Paciente.objects.filter(nomUsuario= user, contraseña = pwd)
    return res

def login(request):
    if request.method=="POST": 
        flogin = FormLogin(data=request.POST)
        if flogin.is_valid():
            user = flogin.cleaned_data['username']
            pwd = flogin.cleaned_data['password']
            tipo = flogin.cleaned_data['tipo']
            if ObtenerTipo(user, pwd, tipo):
                payload = {
                    'id': user,
                    'tipo': tipo,
                }

                jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
                return render(request, "Usuarios/funciona.html", {'token':json.dumps(jwt_token)})
            else:
                mensaje = "Lo sentimos, no estas en el sistema :("
    else:
        flogin=FormLogin()
    return render(request, "Usuarios/inicioSesion.html", {"form": flogin})

    
