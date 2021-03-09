from django.http import HttpResponse
from django.shortcuts import render


def inicio(request):
    return render(request, "Usuarios/index.html")

def regC(request):
    return render(request, "Usuarios/registroCuidador.html")

def regP(request):
    return render(request, "Usuarios/registroPaciente.html")

def recPasswd(request):
    return render(request, "Usuarios/recuperarC.html")

def login(request):
    return render(request, "Usuarios/inicioSesion.html")

