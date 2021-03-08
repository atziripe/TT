from django.shortcuts import render
from django.http import HttpResponse


def inicioC(request):
    return render(request, "Cuidador/inicioCuidador.html")

def editC(request):
    return render(request, "Cuidador/editarCuidador.html")

def ingrDatosC (request):
    return render(request, "Cuidador/IngresarDatosCuidador.html")
