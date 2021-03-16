from django.http import HttpResponse
from django.shortcuts import render
from Usuarios.forms import FormLogin #API Forms
from Pruebas.models import Paciente
from Cuidador.models import Cuidador
from Especialista.models import Especialista
from Administrador.models import Administrador
from django_cryptography.fields import encrypt
import jwt, json


def inicio(request):
    return render(request, "Usuarios/index.html")

def regC(request):
    return render(request, "Usuarios/registroCuidador.html")

def regP(request):
    return render(request, "Usuarios/registroPaciente.html")

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
                #return render(request, "Usuarios/funciona.html")
            else:
                mensaje = "Lo sentimos, no estas en el sistema :("
    else:
        flogin=FormLogin()
    return render(request, "Usuarios/inicioSesion.html", {"form": flogin})

    
