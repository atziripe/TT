from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from Administrador.forms import FormEditarA, FormEditarRelacionesP
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User, Group
from Usuario import views
#from django.db import models
from django.urls import reverse_lazy
import re, json, jwt, requests


def inicioA(request, token):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        return render(request, "Administrador/inicioAdministrador.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': "Administrador"})
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html", {"session_expired": True} )


def editA(request, token, tipo, name):
    try:
        base = "Administrador/baseAdministrador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        print("iduser", iduser)
        infoU = requests.get('http://127.0.0.1:8000/v1/userd/'+str(iduser)+'')
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
                    print("No se pudo hacer la edición del usuario")
                    return render(request, "Administrador/editarAdministrador.html", {"name":feditA.cleaned_data['nvo_nombre'], "form": feditA, "user": iduser, "access": token, "tipo": tipo, "already_exists": True, "base": base})

        else:
            feditA=FormEditarA(initial=initial_dict)
        return render(request, "Administrador/editarAdministrador.html", {"name": name, "form": feditA, "user": iduser, "access": token, "tipo": tipo, "base": base}) #Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html", {"session_expired": True})



def obtenerInfoUsers(usersID_req, user_type): #Para cada tipo de usuario se genera lista de usuarios del grupo y se añade la indicación de a qué grupo pertenecen
    lista_infoU = {}
    usersID = json.loads(usersID_req.content)

    for user in usersID:
        cuidador_uname = -1 #Inicializamos a -1 estas dos variables que seran para el paciente sin relaciones con otros usuarios
        especialista_uname = -1
        id_user = user['user']
        infoU_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user)+'')
        infoU = json.loads(infoU_req.content)   #Json en django viene siendo como un diccionario
        lista_infoU[infoU['username']] = infoU  #En este punto, añadimos un usuario a la lista identificándolo con su username
        lista_infoU[infoU['username']]["user_type"] = user_type #Añadimos tipo de usuario

        if user_type == "Paciente": #Para el usuario paciente, necesitamos más datos...
            info_user = list(Paciente.objects.filter(user_id=id_user).values())
            for dato in info_user:
                cuidador_id = dato['cuidador_id']
                especialista_id = dato['especialista_id']

            cuidador_info = list(Cuidador.objects.filter(id=cuidador_id).values())
            for dato in cuidador_info:
                cuidador_idUser = dato['user_id']
                cuidador_uname = User.objects.get(id=cuidador_idUser).username
                
            especialista_info = list(Especialista.objects.filter(id=especialista_id).values())
            for dato in especialista_info:
                especialista_idUser = dato['user_id']
                especialista_uname = (User.objects.get(id=especialista_idUser).first_name + ' ' + User.objects.get(id=especialista_idUser).last_name)
                
            lista_infoU[infoU['username']]["cuidador"] = cuidador_uname #Entonces los añadimos a lista
            lista_infoU[infoU['username']]["especialista"] = especialista_uname

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
        return render(request, "Usuarios/index.html", {"session_expired": True})


def editarRelacionesP(request, token, tipo, name, paciente):
    base = "Administrador/baseAdministrador.html"
    try:
        infoP = requests.get('http://127.0.0.1:8000/v1/Pacienteuser/'+str(paciente)+'')
        sinDoctor = False; doctorActual = -1; Modificacion_Doctor = True; doctorNuevo_numPac= -1
        if infoP.ok:
            initial_dict = {
                "nvo_cuidador":json.loads(infoP.content)['cuidador'],
                "nvo_especialista": json.loads(infoP.content)['especialista']
            }
        else:
            print("Ocurrio error en paciente ", infoP.status_code)
        if request.method=="POST": 
            feditRP = FormEditarRelacionesP(request.POST, initial=initial_dict)   
            if feditRP.is_valid(): 
                payloadP = {
                    "cuidador":feditRP.cleaned_data['nvo_cuidador'],
                    "especialista":feditRP.cleaned_data['nvo_especialista'],
                    "sexo": json.loads(infoP.content)['sexo'],
                    "escolaridad": json.loads(infoP.content)['escolaridad'],
                    "fechaDiag": json.loads(infoP.content)['fechaDiag']
                    }
                #Para poder hacer la actualización, tenemos que tomar en cuenta que el especialista que vamos a añadir aún tenga disponibilidad de atender a más pacientes
                if payloadP['especialista']!="Ninguno":
                    doctorNuevo = int(payloadP['especialista'])
                    try:
                        doctorActual = int(json.loads(infoP.content)['especialista'])
                    except:
                        sinDoctor = True #Comprobamos si se tenia o no doctor asignado, si es así, actualizaremos su número de pacientes

                    #En los dos bucles siguientes se captura el id user de los doctores para la modificacion de sus datos
                    doctorNuevo_datos= list(Especialista.objects.filter(id=feditRP.cleaned_data['nvo_especialista']).values())
                    for dato in doctorNuevo_datos:
                        doctorNuevo_IdUser = dato['user_id']
                        doctorNuevo_numPac = dato['numPacientes']

                    if not sinDoctor: 
                        doctorActual_datos=list(Especialista.objects.filter(id=doctorActual).values())
                        for dato in doctorActual_datos:
                            doctorActual_IdUser = dato['user_id']

                    #Si ya se llego al limite de pacientes que admite un especialista, no nos deja hacer la operación
                    if (doctorNuevo_numPac > 0) or (doctorNuevo == doctorActual):
                        print(payloadP)

                        if doctorNuevo == doctorActual: #Si no se modifica doctor, nos saltamos cambios a numPacientes
                            Modificacion_Doctor= False
                        
                        if Modificacion_Doctor: #Si el paciente tenia doctor y era otro al que estamos asignado, actualizamos npacientes de ambos
                            if not sinDoctor:
                                infoE_Actual = requests.get('http://127.0.0.1:8000/v1/Especialistauser/'+str(doctorActual_IdUser)+'')
                            infoE_Nuevo = requests.get('http://127.0.0.1:8000/v1/Especialistauser/'+str(doctorNuevo_IdUser)+'')
                            
                            if infoE_Nuevo.ok:
                                if not sinDoctor:
                                    payloadEspecialista_Actual = {
                                        "numPacientes": json.loads(infoE_Actual.content)['numPacientes'] + 1,
                                        "datos_generales": json.loads(infoE_Actual.content)['datos_generales']
                                    }
                                payloadEspecialista_Nuevo = {
                                    "numPacientes": json.loads(infoE_Nuevo.content)['numPacientes'] - 1,
                                    "datos_generales": json.loads(infoE_Nuevo.content)['datos_generales']
                                }
                        #A estas alturas corremos la actualizacion de los datos del paciente
                        updateP =requests.put('http://127.0.0.1:8000/v1/editarpaciente/'+str(json.loads(infoP.content)['id']) +'', data=json.dumps(payloadP), headers={'content-type': 'application/json'})
                        if updateP.ok:
                            print("Actualizacion correcta de datos del paciente")
                        else:
                            print(updateP)
                            if ("cuidador" in json.loads(updateP.content)): #Error en el cuidador
                                return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio":False, "errorERP_Care": True})
                            if ("especialista" in json.loads(updateP.content)): #Error en el especialista
                                return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio":False, "errorERP_Doctor": True})
                        
                        #Si no hubo problemas con los datos pasados, actualizamos nPacientes de los doctores
                        if Modificacion_Doctor:
                            if not sinDoctor:
                                updateE_Actual_nPac = requests.put('http://127.0.0.1:8000/v1/editarespecialista/'+str(json.loads(infoE_Actual.content)['id'])+'', data=json.dumps(payloadEspecialista_Actual), headers={'content-type': 'application/json'})
                            updateE_Nuevo_nPac = requests.put('http://127.0.0.1:8000/v1/editarespecialista/'+str(json.loads(infoE_Nuevo.content)['id'])+'', data=json.dumps(payloadEspecialista_Nuevo), headers={'content-type': 'application/json'})
                                
                            if updateE_Nuevo_nPac.ok:
                                print("¡Modificacion de numero de pacientes correcta!")
                                return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio": False, "successfulERP": True}) 
                            else:
                                return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio":False, "errorERP_Doctor": True}) 
                        else: #Si no hubo modificación de doctor, nos vamos directo a terminar la operación
                                print("No hubo modificación de datos respecto a doctor")
                                return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio": False, "successfulERP": True}) 
                    else:
                        print("El especialista ya no puede atender más pacientes")
                        return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio":False, "errorERP_D_MaxP": True})          
                else:
                    return render(request, "Administrador/editarRelacionesPaciente.html", {"form": feditRP, "name": name, "tipo": tipo, "base": base, "access": token, "paciente": paciente, "inicio":False, "errorERP_Doctor": True})
            else:
                print("No se pudo hacer la modificación propuesta")
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
            try:
                Doctor_de_Pa_ID = Paciente.objects.get(user_id=e_usuario).especialista_id
                Doctor_de_Pa = Especialista.objects.get(id=Doctor_de_Pa_ID)
                Doctor_de_Pa.numPacientes += 1
                Doctor_de_Pa.save()
            except:
                print("El paciente no tenia especialista asignado")

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
            print("Se va a eliminar un administrador")

        if Usuario_SinPaciente:
            usuario.groups.clear() #Quitamos al usuario del grupo donde esté y luego lo borramos
            usuario.delete()
            print("El usuario ha sido eliminado con exito")

            if int(id_admin_Actual) == int(e_usuario): #Si eliminamos a nuestro propio usuario, nos aparece un aviso diferente
                return render(request, "Administrador/eliminarPerfil.html", {"access": token, "tipo":tipo, "name":name, "e_usuario":e_usuario, "e_username": e_username, "user_deleted": True})
            else:
                return render(request, "Administrador/eliminarPerfil.html", {"access": token, "tipo":tipo, "name":name, "e_usuario":e_usuario, "e_username": e_username, "successfull_delete": True})
    else:
        return render(request, "Administrador/eliminarPerfil.html", {"access": token, "tipo":tipo, "name":name, "e_usuario":e_usuario, "e_username": e_username})