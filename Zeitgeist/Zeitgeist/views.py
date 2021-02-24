from django.http import HttpResponse
from django.shortcuts import render


def inicioPa(request):
    return render(request, "inicioPaciente.html")

def inicioC(request):
    return render(request, "inicioCuidador.html")

def inicio(request):
    return render(request, "index.html")



