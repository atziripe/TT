from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .forms import FormEditarA, FormModificarRelacion
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User
from Usuario import views
#from django.db import models
from django.urls import reverse_lazy
import re, json, jwt, requests

# Create your views here.

def inicioA(request):
    try:
        return render(request, "Administrador/inicioAdministrador.html")
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html")


def editA(request, token):
    try:
        base = "Administrador/baseAdministrador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        print("iduser", iduser)
        infoU = requests.get('http://127.0.0.1:8000/v1/userd/'+str(iduser)+'')
        #infoA = requests.get('http://127.0.0.1:8000/v1/AdministradorUser/'+str(iduser)+'')
        if infoU.ok:
            initial_dict = {
                "nvo_nombre":json.loads(infoU.content)['first_name'],
                "nvo_apellidos": json.loads(infoU.content)['last_name'],
                "nvo_nombreUsuario":json.loads(infoU.content)['username'],
                "nvo_correo":json.loads(infoU.content)['email']  
            }
        else:
            print("Ocurrio error en usuario ", infoU.status_code)
        if request.method=="POST": 
            feditA = FormEditarA(request.POST, initial=initial_dict)
            #try:      
            if feditA.is_valid(): 
                payload = {
                    "username": feditA.cleaned_data['nvo_nombreUsuario'],
                    "first_name": feditA.cleaned_data['nvo_nombre'],
                    "last_name": feditA.cleaned_data['nvo_apellidos'],
                    "email": feditA.cleaned_data['nvo_correo']
                }
                updateU =  requests.put('http://127.0.0.1:8000/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
                           payload), headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
                if updateU.ok:
                    print("Se pudo actualizar el usuario")
                    return render(request, "Administrador/inicioAdministrador.html", {"name":feditA.cleaned_data['nvo_nombre'], "access": token, "modified" : True})
                else:
                    print(updateU.json())
                    print("No se pudo hacer el registro del usuario")
                    return render(request, "Administrador/editarAdministrador.html", {"form": feditA, "user": iduser, "access": token, "already_exists": True, "base": base})

        else:
            feditA=FormEditarA(initial=initial_dict)
        return render(request, "Administrador/editarAdministrador.html", {"form": feditA, "user": iduser, "access": token, "base": base}) #Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html")


def modificarRels(request):
    if request.method == "POST":
        ModRels = FormModificarRelacion(data = request.POST)
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
        EliminarP=FormEliminarPerfil()
    return render(request, "Administrador/eliminarPerfil.html", {"form": fEliminarP})
    