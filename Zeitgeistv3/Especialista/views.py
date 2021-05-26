from django.shortcuts import render,  redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from Usuario import views
from .forms import FormEditarE, FormMensaje
from .models import Mensaje
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User
from Paciente.models import Ap_Screening
import random, re, json, jwt, requests
import string, datetime

def inicioEsp(request, token):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': "Especialista"})
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html", {"session_expired": True})


def editE(request, token, tipo, name):
    try:  
        base = "Especialista/baseEspecialista.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        print("iduser", iduser)
        infoU = requests.get('http://127.0.0.1:8000/v1/userd/'+str(iduser)+'')
        infoE = requests.get('http://127.0.0.1:8000/v1/Especialistauser/'+str(iduser)+'')

        if infoE.ok and infoU.ok:
            initial_dict = {
                "nvo_nombre":json.loads(infoU.content)['first_name'],
                "nvo_apellidos": json.loads(infoU.content)['last_name'],
                "nvo_correo":json.loads(infoU.content)['email'],
                "nvos_datos_generales":json.loads(infoE.content)['datos_generales'],
                "nvo_numPacientes":json.loads(infoE.content)['numPacientes'], 
            }
        else:
            print("Ocurrio error en usuario", infoU.status_code)
            print("Ocurrio error en especialista", infoE.status_code)
        if request.method=="POST": 
            feditE = FormEditarE(request.POST, initial=initial_dict)
            #try:      
            if feditE.is_valid(): 
                payload = {
                    "first_name": feditE.cleaned_data['nvo_nombre'],
                    "last_name": feditE.cleaned_data['nvo_apellidos'],
                    "username": json.loads(infoU.content)['username'],
                    "email": feditE.cleaned_data['nvo_correo']
                }
                updateU =  requests.put('http://127.0.0.1:8000/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
                            payload), headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
                if updateU.ok:
                    print("Se pudo actualizar el usuario")
                    payloadE = {
                        "datos_generales":feditE.cleaned_data['nvos_datos_generales'],
                        "numPacientes":feditE.cleaned_data['nvo_numPacientes'],
                    }
                    print(payloadE)
                    updateE =requests.put('http://127.0.0.1:8000/v1/editarespecialista/'+str(json.loads(infoE.content)['id']) +'', data=json.dumps(payloadE), headers={'content-type': 'application/json'})
                    if updateE.ok:
                        return render(request, "Especialista/inicioEspecialista.html", {"name":feditE.cleaned_data['nvo_nombre'], "tipo": tipo, "access": token, "modified" : True})
                    else:
                        print(updateE.json())
                else:
                    print(updateU.json())
                    print("No se pudo hacer el registro del usuario")
                    return render(request, "Especialista/editarEspecialista.html", {"name":feditE.cleaned_data['nvo_nombre'],"form": feditE, "user": iduser, "access": token, "tipo": tipo, "already_exists": True, "base": base})

        else:
            feditE=FormEditarE(initial=initial_dict)
        return render(request, "Especialista/editarEspecialista.html", {"name": name, "form": feditE, "user": iduser, "base": base, "tipo": tipo, "access": token}) #Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html")


def cveAcceso(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    try: 
        if request.method=="POST":
            userp = User.objects.filter(username=request.POST['nomUsu'])[0].id
            print("userp ", userp)
            pacient = Paciente.objects.filter(user_id=userp)[0]
            print("pacient ", pacient)
            decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = decodedToken['user_id']
            fecha = datetime.datetime.now()
            fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
            clave = str(fecha.day)+str(fecha.month)+str(fecha.year)[2:4]+str(fecha.hour)+str(fecha.minute)+str(user)+random.choice(string.ascii_uppercase)+str(random.randint(0,9))+random.choice(string.ascii_uppercase)
            print(clave)
            if Ap_Screening.objects.filter(resultadoFinal__isnull=True ,paciente=pacient): 
                print("No se pudo crear la sesión de tamizaje")
                return render(request, "Especialista/inicioEspecialista.html",{"exito": 'false', 'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})
            else:
                screening = Ap_Screening.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy)
                screening.save()
                print(clave)
                return render(request, "Especialista/inicioEspecialista.html",{'clave':clave, 'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})
    except:
        print("El paciente indicado no es atendido por este especialista")
        return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': tipo, 'error_paciente': True})
    return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})


def obtenerInfoUsers(usersIDList_req, idEspecialista): #Obtenemos la informacion de los pacientes del especialista, incluyendo notificación si no tienen cuidador 
    lista_infoP = {}
    usersID = json.loads(usersIDList_req.content)
    escolaridad_values ={ 'N':'Ninguna', 'PR':'Primaria', 'SC':'Secundaria', 'BCH':'Bachillerato', 'SUP':'Licenciatura o superior'}
    sexo_values = {'F': "Femenino", 'M': "Masculino"}

    for user in usersID:
        cuidador_uname = -1 #Inicializamos a -1 estas dos variables que seran para el paciente sin relaciones con otros usuarios
        id_paciente = user['id'] #Id de usuario de paciente
        infoP_req = requests.get('http://127.0.0.1:8000/v1/pacientsd/'+str(id_paciente)+'')
        doctor_dePa = json.loads(infoP_req.content)['especialista']

        if int(doctor_dePa) == int(idEspecialista):
            infoP = json.loads(infoP_req.content)  #Sacamos datos del paciente si fue asignado al especialista
            id_user_Pa = infoP['user']
            infoUserP_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user_Pa)+'')
            infoUserP = json.loads(infoUserP_req.content)
            
            lista_infoP[infoUserP['username']] = infoUserP
            lista_infoP[infoUserP['username']]['idPaciente'] = infoP['id']
            lista_infoP[infoUserP['username']]['sexo'] = sexo_values[infoP['sexo']]
            fechaNac_date = datetime.datetime.strptime(infoP['fechaNac'], '%Y-%m-%d') 
            lista_infoP[infoUserP['username']]['fechaNac'] = fechaNac_date.strftime('%d / %m / %Y')
            lista_infoP[infoUserP['username']]['escolaridad'] = escolaridad_values[infoP['escolaridad']]
            fechaDiag_date = datetime.datetime.strptime(infoP['fechaDiag'], '%Y-%m-%d') 
            lista_infoP[infoUserP['username']]['fechaDiag'] = fechaDiag_date.strftime('%d / %m / %Y')

            id_cuidador = json.loads(infoP_req.content)['cuidador'] #Obtenemos nombre completo del Cuidador de cada paciente
            id_user_c = Cuidador.objects.get(id=id_cuidador).user_id
            infoCui_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user_c)+'')
            cuidador_name = json.loads(infoCui_req.content)['first_name'] + ' ' + json.loads(infoCui_req.content)['last_name']
                
            lista_infoP[infoUserP['username']]["cuidador_name"] = cuidador_name

    return lista_infoP 
    

def verPacientes(request, token, tipo):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        idEspecialista = Especialista.objects.get(user_id=iduser).id #Obtenemos ID de user

        if not Paciente.objects.filter(especialista=idEspecialista).exists(): #Si no tenemos pacientes, no se genera tabla 
            return render(request, "Especialista/visualizarPacientes.html", {'No_tiene_pacientes': True, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, "base": "Especialista/baseEspecialista.html"})
        else:
            pacientesIDlist_req = requests.get('http://127.0.0.1:8000/v1/listpacient/', headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
            listaPacientes = obtenerInfoUsers(pacientesIDlist_req, idEspecialista)
            return render(request, "Especialista/visualizarPacientes.html", {"listPatients": listaPacientes, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, "base": "Especialista/baseEspecialista.html"})
    except:
        print("Error de autenticación")
        return render(request, "Usuarios/index.html", {"session_expired": True})



def mensajeCuidador(request, token, tipo, pacienteC):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser_Esp = decodedToken['user_id']
        esp_inst = Especialista.objects.get(user_id=iduser_Esp)
        fecha = datetime.datetime.now()
        fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)

        infoPaciente = requests.get('http://127.0.0.1:8000/v1/pacientsd/'+str(pacienteC)+'')
        id_cuidador = json.loads(infoPaciente.content)['cuidador'] #Obtenemos nombre de usuario y nombre completo del Cuidador 
        cui_inst= Cuidador.objects.get(id=id_cuidador)
        id_user_c = cui_inst.user_id
        infoCui_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user_c)+'')
        cuidador_name = json.loads(infoCui_req.content)['first_name'] + ' ' + json.loads(infoCui_req.content)['last_name']       
        initial_dict = { "cuidador": cuidador_name}

        if request.method=="POST": 
            fmsg = FormMensaje(request.POST, initial=initial_dict)
                
            if fmsg.is_valid(): 
                mensaje = Mensaje.objects.create(especialista=esp_inst, cuidador=cui_inst,  mensaje= fmsg.cleaned_data['mensaje'],fechaEnvio=fechahoy)
                mensaje.save()
                return render(request, "Especialista/mensajesCuidador.html", {'form': fmsg, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, 'success_sentM': True, 'base': "Especialista/baseEspecialista.html"})
            else:
                return render(request, "Especialista/mensajesCuidador.html", {'form': fmsg, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, 'error_sentM': True, 'base': "Especialista/baseEspecialista.html"})
            
        else:
            fmsg=FormMensaje(initial=initial_dict)
            return render(request, "Especialista/mensajesCuidador.html", {'form': fmsg, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, 'initial': True, 'base': "Especialista/baseEspecialista.html"})
    
    except:
        print("Error en la vista de mensajes del cuidador")
        return render(request, "Usuarios/index.html", {"session_expired": True})
