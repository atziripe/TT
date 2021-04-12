from django.shortcuts import render
from django.http import HttpResponse

def inicioEsp(request):
    return render(request, "Especialista/inicioEspecialista.html")

#def editEsp(request):
 #   return render(request, "Especialista/editarEspecialista.html")

