from django.http import HttpResponse
from django.shortcuts import render


def inicioPa(request):
    return render(request, "inicioPaciente.html")

def inicioC(request):
    return render(request, "inicioCuidador.html")

def inicio(request):
    return render(request, "index.html")

def rmsc1(request):
    return render(request, "reminiscencia1.html")

def rmsc2(request):
    return render(request, "reminiscencia2.html")

def rmsc3(request):
    return render(request, "reminiscencia3.html")

def editC(request):
    return render(request, "editarCuidador.html")

def editP(request):
    return render(request, "editarPaciente.html")

def regC(request):
    return render(request, "registroCuidador.html")

def regP(request):
    return render(request, "registroPaciente.html")

def recPasswd(request):
    return render(request, "recuperarC.html")

def ingrDatosC (request):
    return render(request, "IngresarDatosCuidador.html")
