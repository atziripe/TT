from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.auth.models import User

# Create your views here.

def inicioA(request):
    return render(request, "Administrador/inicioAdministrador.html", )

