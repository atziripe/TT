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