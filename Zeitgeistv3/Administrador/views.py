from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .forms import FormEditarA, FormEditarRelacionesP
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User, Group
from Usuario import views
#from django.db import models
from django.urls import reverse_lazy
import re, json, jwt, requests

# Create your views here.

def inicioA(request, token):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        return render(request, "Administrador/inicioAdministrador.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': "Administrador"})
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html")


def editA(request, token, tipo, name):
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
                    return render(request, "Administrador/inicioAdministrador.html", {"name":feditA.cleaned_data['nvo_nombre'], "access": token, "tipo": tipo, "modified" : True})
                else:
                    print(updateU.json())
                    print("No se pudo hacer el registro del usuario")
                    return render(request, "Administrador/editarAdministrador.html", {"name":feditA.cleaned_data['nvo_nombre'], "form": feditA, "user": iduser, "access": token, "tipo": tipo, "already_exists": True, "base": base})

        else:
            feditA=FormEditarA(initial=initial_dict)
        return render(request, "Administrador/editarAdministrador.html", {"name": name, "form": feditA, "user": iduser, "access": token, "tipo": tipo, "base": base}) #Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html")

def obtenerInfoUsers(usersID_req, user_type): #Para cada tipo de usuario se genera lista de usuarios del grupo y se añade la indicación de a qué grupo pertenecen
    lista_infoU = {}
    usersID = json.loads(usersID_req.content)

    for user in usersID:
        id_user = user['user']
        infoU_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user)+'')
        infoU = json.loads(infoU_req.content)   #Json en django viene siendo como un diccionario
        lista_infoU[infoU['username']] = infoU  #En este punto, añadimos un usuario a la lista identificándolo con su username
        lista_infoU[infoU['username']]["user_type"] = user_type #Añadimos tipo de usuario
    #print(lista_infoUsers), retornamos lista de usuarios del tipo
    return lista_infoU
    

def modificarEliminarU(request, token, tipo, name):
    try:
        base = "Administrador/baseAdministrador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        
        #Se genera lista de usuarios con su tipo respectivo
        adminsID_req = requests.get('http://127.0.0.1:8000/v1/listadmins/', headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
        cuidadoresID_req = requests.get('http://127.0.0.1:8000/v1/listcare/', headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})    
        especialistasID_req = requests.get('http://127.0.0.1:8000/v1/listspecialist/', headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
        pacientesID_req = requests.get('http://127.0.0.1:8000/v1/listpacient/', headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
        
        listAdmins = obtenerInfoUsers(adminsID_req, "Administrador") 
        listCuidadores = obtenerInfoUsers(cuidadoresID_req, "Cuidador")
        listaEspecialistas = obtenerInfoUsers(especialistasID_req, "Especialista")
        listaPacientes = obtenerInfoUsers(pacientesID_req, "Paciente")

        listaOtrosUsr = listAdmins #Creación de la lista que tendrá a todos los usuarios que no son Pacientes
        listaOtrosUsr.update(listCuidadores)
        listaOtrosUsr.update(listaEspecialistas)

        #print(listaOtrosUsr)
        #for user in listAdmins:
        #    print("Nombre de Usuario: "+listAdmins[user]['username']+", Nombre completo: "+ listAdmins[user]['first_name']+" "+listAdmins[user]['last_name']+", Tipo de Usuario: "+ listAdmins[user]['user_type'])
        #print("Administradores:");print(listAdmins); print("Cuidadores:");print(listCuidadores); print("Pacientes:");print(listaPacientes)
        
        return render(request, "Administrador/opcionesAdministrador.html", {"listPatients": listaPacientes, "listOUsers": listaOtrosUsr ,"name": name, "tipo": tipo, "base": base, "access": token})
    except:
        print("Error de autenticación")
        return render(request, "Usuarios/index.html")

def editarRelacionesP(request, token, tipo, name, paciente):
    base = "Administrador/baseAdministrador.html"
    infoP = requests.get('http://127.0.0.1:8000/v1/Pacienteuser/'+str(paciente)+'')
    
    if infoP.ok:
        initial_dict = {
            "nvo_cuidador":json.loads(infoP.content)['cuidador'],
            "nvo_especialista": json.loads(infoP.content)['especialista']
        }
    else:
        print("Ocurrio error en paciente ", infoP.status_code)
    if request.method=="POST": 
        feditRP = FormEditarRelacionesP(request.POST, initial=initial_dict)
        try:      
            if feditRP.is_valid(): 
                payloadP = {
                    "cuidador":feditRP.cleaned_data['nvo_cuidador'],
                    "especialista":feditRP.cleaned_data['nvo_especialista'],
                    "sexo": json.loads(infoP.content)['sexo'],
                    "escolaridad": json.loads(infoP.content)['escolaridad'],
                    "fechaDiag": json.loads(infoP.content)['fechaDiag']
                    }
                print(payloadP)
                updateP =requests.put('http://127.0.0.1:8000/v1/editarpaciente/'+str(json.loads(infoP.content)['id']) +'', data=json.dumps(payloadP), headers={'content-type': 'application/json'})
                if updateP.ok:
                    print("actualizacion correcta")
                    return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio": False, "successfulERP": True}) 
                else:
                    print(updateP.json())
                    return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio":False, "errorERP": True})
            else:
                feditRP=FormEditarRelacionesP(initial=initial_dict)
            return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "initial": True})
        except:
            print("Error en pagina de edición de relaciones del paciente")
        return render(request, "Usuarios/index.html", {"session_expired": True})
        
def eliminarU(request, token, tipo, name, e_usuario, e_username):
    base = "Administrador/baseAdministrador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
    if request.method=="POST": 
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        id_admin_Actual = decodedToken['user_id']
        usuario = User.objects.get(id= e_usuario)
        Usuario_SinPaciente = True

        if User.objects.filter(id=e_usuario, groups__name='Pacientes').exists():
            print("Se va a eliminar un paciente") 
            #No hay necesidad de hacer cambio a su cuidador: puede volver a ser asignado a otro paciente. Pero debemos cambiar el numPacientes del Doctor asociado
            Doctor_de_Pa_ID = Paciente.objects.get(user_id=e_usuario).especialista_id
            Doctor_de_Pa = Especialista.objects.get(id=Doctor_de_Pa_ID)
            Doctor_de_Pa.numPacientes += 1
            Doctor_de_Pa.save()

        elif User.objects.filter(id=e_usuario, groups__name='Cuidadores').exists():
            cuidador_ID = Cuidador.objects.get(user=e_usuario).id
            if Paciente.objects.filter(cuidador=cuidador_ID).exists():
                Usuario_SinPaciente = False    #No puede eliminarse Cuidador si tiene paciente asignado
                return render(request, "Administrador/eliminarPerfil.html", {"access": token, "tipo":tipo, "name":name, "e_usuario":e_usuario, "e_username": e_username, "errorDel_Care": True})

        elif User.objects.filter(id=e_usuario, groups__name='Especialistas').exists():
            print("Se va a eliminar un especialista")
            especialista_ID = Especialista.objects.get(user=e_usuario).id
            if Paciente.objects.filter(especialista=especialista_ID).exists():
                Usuario_SinPaciente = False    #No puede eliminarse Especialista si tiene pacientes a su cargo
                return render(request, "Administrador/eliminarPerfil.html", {"access": token, "tipo":tipo, "name":name, "e_usuario":e_usuario, "e_username": e_username, "errorDel_Doctor": True})
            
    else:
        feditRP=FormEditarRelacionesP(initial=initial_dict)
    
    return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "initial": True})



