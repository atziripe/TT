from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FormEditarA, FormModificarRelacion, FormEliminarPerfil
from .models import Administrador
from Pruebas.models import Paciente
from Cuidador.models import Cuidador
from Especialista.models import Especialista
from django.contrib.auth.models import User
from Usuarios import views
#from django.db import models
from django.urls import reverse_lazy
import re

# Create your views here.

def inicioA(request):
    return render(request, "Administrador/inicioAdministrador.html")
    #return render(request, "Usuarios/index.html")

def editA(request):
    base = "Administrador/baseAdministrador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
    try:
        adminActual = Administrador.objects.get(nomUsuario= request.session.get("usuarioActual"))
    except:
         return render(request, "Usuarios/index.html")

    if request.method=="POST": 
        feditA = FormEditarA(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if feditA.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',request.POST['nvo_correo'].lower()): #Validación de formulario y correo electrónico
                pwd = request.POST['nvo_contrasena']
                curr_pwd = request.POST['confirmacion_cont']
                nomUser = request.POST['nvo_nombreUsuario']

                if nomUser != adminActual.nomUsuario: #Si el nombre de usuario no se modifico, nos saltamos validación de existencia.
                    if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                        return redirect("/administrador/editarA/?ya_existe_registro")
                
                pass_valida = views.ValidarContrasena(pwd) #Validacion de contraseña:
                if pass_valida == False:
                    return redirect("/administrador/editarA/?contrasena_invalida")
            else:
                return redirect("/administrador/editarA/?no_valido")        
	        #Checar que contraseña actual es correcta
            if curr_pwd == adminActual.contrasena:
	            #Si coincide, se aplica el cambio solicitado

                adminActual.nomUsuario = nomUser
                adminActual.nombre=request.POST['nvo_nombre']
                adminActual.contrasena= pwd
                adminActual.correo=request.POST['nvo_correo']
                adminActual.save()

                return redirect("/login/?edicion_valida")
            else:
                return redirect("/administrador/editarA/?error_contrasena")
        except:
            return redirect("/administrador/editarA/?no_valido")
    else:
        feditA=FormEditarA()
    return render(request, "Administrador/editarAdministrador.html", {"form": feditA, "base": base}) #Renderizar vista pasando el formulario como contexto

def modificarRels(request):
    if request.method == "POST":
        fModRels = FormModificarRelacion(data = request.POST)
        if fModRels.is_valid():
            paciente = request.POST.get("paciente")

            if Paciente.objects.filter(nomUsuario=paciente) or Paciente.objects.filter(nombre=paciente):
                return redirect("/administrador/modificarRelaciones/?valido")
            else: 
                return redirect("/administrador/modificarRelaciones/?no_valido")
    else:
        fModRels=FormModificarRelacion()
    return render(request, "Administrador/modificarRelaciones.html", {"form": fModRels})

def eliminarPerfs(request):
    if request.method == "POST":
        fEliminarP = FormEliminarPerfil(data = request.POST)
        if fEliminarP.is_valid():
            perfil = request.POST.get("perfil")

            if Administrador.objects.filter(nomUsuario=perfil):
                if perfil == request.session.get("usuarioActual"):
                    return redirect("/administrador/eliminarPerfiles/?borrarseASiMismo")
                else:
                    return redirect("/administrador/eliminarPerfiles/?borrarAdmin")  

            if Paciente.objects.filter(nomUsuario=perfil) or Especialista.objects.filter(nomUsuario=perfil) or Cuidador.objects.filter(nomUsuario=perfil):
                return redirect("/administrador/eliminarPerfiles/?borrarUsuario")
            else: 
                return redirect("/administrador/eliminarPerfiles/?no_existe")
    else:
        fEliminarP=FormEliminarPerfil()
    return render(request, "Administrador/eliminarPerfil.html", {"form": fEliminarP})