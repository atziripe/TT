from django.http import HttpResponse
from django.shortcuts import render


def inicio(request):
    return render(request, "index.html")

def regC(request):
    return render(request, "registroCuidador.html")

def regP(request):
    return render(request, "registroPaciente.html")

def recPasswd(request):
    return render(request, "recuperarC.html")

def login(request):
    return render(request, "inicioSesion.html")

