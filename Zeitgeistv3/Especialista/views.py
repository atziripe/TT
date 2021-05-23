from django.shortcuts import render,  redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from Usuario import views
from .forms import FormEditarE
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User
from Paciente.models import Ap_Screening
import random, re, json, jwt, requests
import string, datetime


def inicioEsp(request):
    try:
        return render(request, "Especialista/inicioEspecialista.html")
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html")

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


