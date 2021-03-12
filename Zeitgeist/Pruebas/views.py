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

def moca1(request):
    return render(request, "Pruebas/tamizaje1.html")

def moca2(request):
    return render(request, "Pruebas/tamizaje2.html")

def moca3(request):
    return render(request, "Pruebas/tamizaje3.html")

def moca4(request):
    return render(request, "Pruebas/tamizaje4.html")

def editP(request):
    return render(request, "Pruebas/editarPaciente.html")