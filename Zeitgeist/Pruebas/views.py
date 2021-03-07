from django.shortcuts import render
from django.http import HttpResponse

def inicioPa(request):
    return render(request, "Pruebas/inicioPaciente.html")

def rmsc1(request):
    return render(request, "Pruebas/reminiscencia1.html")

def rmsc2(request):
    return render(request, "Pruebas/reminiscencia2.html")

def rmsc3(request):
    return render(request, "Pruebas/reminiscencia3.html")

def editP(request):
    return render(request, "Pruebas/editarPaciente.html")