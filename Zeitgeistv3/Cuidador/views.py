from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Pregunta, Cat_Pregunta
from Usuario.models import Cuidador, Paciente
from Paciente.models import Reminiscencia, Ap_Reminiscencia
from django.contrib.auth.models import User
from rest_framework import permissions
from Usuario import views
from .forms import FormDatosImg, FormEditarC
import random, datetime, string, re, json, jwt, requests

nomusu = 'atziri99'
#pacient = Paciente.objects.filter(cuidador=nomusu)[0]


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.lower(), b.lower())
    return s


def inicioC(request):
    try:
        return render(request, "Cuidador/inicioCuidador.html", {'user': nomusu})
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html")


def editC(request, token, tipo, name):
    try:   
        base = "Cuidador/baseCuidador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
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
            feditC = FormEditarC(request.POST, initial=initial_dict)
            #try:      
            if feditC.is_valid(): 
                payload = {
                    "username": feditC.cleaned_data['nvo_nombreUsuario'],
                    "first_name": feditC.cleaned_data['nvo_nombre'],
                    "last_name": feditC.cleaned_data['nvo_apellidos'],
                    "email": feditC.cleaned_data['nvo_correo']
                }
                updateU =  requests.put('http://127.0.0.1:8000/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
                           payload), headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
                if updateU.ok:
                    print("Se pudo actualizar el usuario")
                    return render(request, "Cuidador/inicioCuidador.html", {"name":feditC.cleaned_data['nvo_nombre'], "access": token, "tipo": tipo, "modified" : True})
                else:
                    print(updateU.json())
                    print("No se pudo hacer el registro del usuario")
                    return render(request, "Cuidador/editarCuidador.html", {"name":feditC.cleaned_data['nvo_nombre'], "form": feditC, "user": iduser, "access": token, "tipo": tipo, "already_exists": True, "base": base})

        else:
            feditC=FormEditarC(initial=initial_dict)
        return render(request, "Cuidador/editarCuidador.html", {"name": name, "form": feditC, "user": iduser, "access": token, "tipo": tipo, "base": base}) #Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html")

def getcveAcceso(request):
    #ckey = Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True, paciente=pacient)[0].cveAcceso
    #return render(request, "Cuidador/inicioCuidador.html",{"clave":ckey})
    return render(request, "Usuarios/index.html")

def cveAcceso(request, token):
    '''fecha = datetime.datetime.now()
    fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
    nom = nomusu[0:2].upper()
    clave = str(fecha.day)+str(fecha.month)+str(fecha.year)[2:4]+str(fecha.hour)+str(fecha.minute)+nom+random.choice(string.ascii_uppercase)+str(random.randint(0,9))+random.choice(string.ascii_uppercase)
    if Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True ,paciente=pacient): 
        print("No se pudo crear la sesión de reminiscencia")
        return render(request, "Cuidador/inicioCuidador.html",{"exito": 'false'})
    else:
        reminiscencia = Ap_Reminiscencia.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy)
        reminiscencia.save()
        print(clave)
        return render(request, "Cuidador/inicioCuidador.html",{"clave":clave})'''
    return render(request, "Cuidador/inicioCuidador.html", {"access": token})


def ingrDatosC (request):
    preguntas = []
    for i in range(2): #audio
        i = random.randint(1,7)
        #print(i)
        if i in preguntas:
            i = random.randint(1,7)
            #print(i)
            pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
            preguntas.append(pregunta[0])
        else:
            pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
            preguntas.append(pregunta[0])
        #preguntas.append(pregunta[0].reactivo)
        
    for i in range(4): #imagen
        i = random.randint(8,18)
        #print(i)
        if i in preguntas:
            i = random.randint(8,18)
            #print(i)
            pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
            preguntas.append(pregunta[0])
        else:
            pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
            preguntas.append(pregunta[0])
        #preguntas.append(pregunta[0].reactivo)
        
    for i in range(4): #texto
        i = random.randint(19,50)
        #print(i)
        if i in preguntas:
            i = random.randint(19,50)
            #print(i)
            pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
            #preguntas.append(pregunta[0].reactivo)
            preguntas.append(pregunta[0])
        else:
            pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
            preguntas.append(pregunta[0])

    if request.method == 'POST':
        idC = Cuidador.objects.get(nomUsuario=nomusu)
        idReact = Cat_Pregunta()
        idReact.idReactivo= request.POST.get('idR')
        pregunta = Pregunta()
        pregunta.idReactivo = idReact
        pregunta.idCuidador = idC
        pregunta.imagen = request.FILES.get('img')
        pregunta.audio = request.FILES.get('aud')
        pregunta.respuestaCuidador = normalize(request.POST.get('respuesta').lower())

        try:
            pregunta.save()
            print("Guardado")
        except:
            print("Error")
   
    return render(request, "Cuidador/IngresarDatosCuidador.html",{'preguntas':preguntas})

def ingresarDatos (request):
    preguntas = []
    i = random.randint(1,79)
    #print(i)
    pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
    preguntas.append(pregunta[0])
     
    if request.method == 'POST':
        #print("entro post")
        idC = Cuidador.objects.get(nomUsuario=nomusu)
        idReact = Cat_Pregunta()
        idReact.idReactivo= request.POST.get('idR')
        preguntaG = Pregunta()
        preguntaG.idReactivo = idReact
        preguntaG.idCuidador = idC
        preguntaG.imagen = request.FILES.get('img')
        preguntaG.audio = request.FILES.get('aud')
        respuesta = request.POST.get('respuesta')
        respuesta2 = request.POST.get('respuesta2')
        respuesta3 = request.POST.get('respuesta3')
        correcta = request.POST.get('correcta')
        print(respuesta)
        print(respuesta2)
        print(respuesta3)
        print(correcta)

        if respuesta2 == None:
            preguntaG.respuestaCuidador = respuesta
        else:
            if correcta == '1':
                print("Entre al primero")
                respuestaf = '1-' + respuesta + '-' + respuesta2 + '-' + respuesta3
                preguntaG.respuestaCuidador = respuestaf
            elif correcta == '2':
                print("Entre al segundo")
                respuestaf = '2-' + respuesta + '-' + respuesta2 + '-' + respuesta3
                preguntaG.respuestaCuidador = respuestaf
            else:
                print("Entre al tercero")
                respuestaf = '3-' + respuesta + '-' + respuesta2 + '-' + respuesta3
                preguntaG.respuestaCuidador = respuestaf
        

        try:
            if preguntaG.save():
                print("Guardado")
        except:
            print("Error")
    return render(request, "Cuidador/ingresarDatos.html",{'preguntas':preguntas})

