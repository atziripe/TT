from django.http import HttpResponse
from django.shortcuts import render

def inicioC(request):
    return render(request, "inicioCuidador.html")

def inicio(request):
    return render(request, "index.html")

def editC(request):
    return render(request, "editarCuidador.html")

def regC(request):
    return render(request, "registroCuidador.html")

def regP(request):
    return render(request, "registroPaciente.html")

def recPasswd(request):
    return render(request, "recuperarC.html")

def ingrDatosC (request):
    return render(request, "IngresarDatosCuidador.html")
