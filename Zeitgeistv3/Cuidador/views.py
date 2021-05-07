from django.shortcuts import render
from .models import Pregunta, Cat_Pregunta
from django.conf import settings
from Usuario.models import Cuidador, Paciente
from Paciente.models import Reminiscencia, Ap_Reminiscencia
from django.contrib.auth.models import User
from rest_framework import permissions
import random
import string
import datetime
import jwt

user = 0

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


def inicioC(request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    return render(request, "Cuidador/inicioCuidador.html",{'name': decodedToken['first_name'], 'access':token})

def editC(request):
    return render(request, "Cuidador/editarCuidador.html")

def getcveAcceso(request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    userc = Cuidador.objects.filter(user_id=user)[0]
    if  Pregunta.objects.filter(idCuidador_id=userc).count() < 10:
        return render(request, "Cuidador/inicioCuidador.html",{"noanswers": 'true', 'name': decodedToken['first_name'], 'access':token})
    else:
        pacient = Paciente.objects.filter(cuidador=userc)[0]
        ckey = Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True, paciente=pacient)[0].cveAcceso
        return render(request, "Cuidador/inicioCuidador.html",{"clave":ckey, 'name': decodedToken['first_name'], 'access':token})

def cveAcceso(request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    userc = Cuidador.objects.filter(user_id=user)[0]
    if  Pregunta.objects.filter(idCuidador_id=userc).count() < 10:
        return render(request, "Cuidador/inicioCuidador.html",{"noanswers": 'true', 'name': decodedToken['first_name'], 'access':token})
    else:
        pacient = Paciente.objects.filter(cuidador=userc)[0] #ide del paciente relacionado con el cuidador
        fecha = datetime.datetime.now()
        fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
        clave = str(fecha.day)+str(fecha.month)+str(fecha.year)[2:4]+str(fecha.hour)+str(fecha.minute)+str(user)+random.choice(string.ascii_uppercase)+str(random.randint(0,9))+random.choice(string.ascii_uppercase)
        if Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True ,paciente=pacient): 
            print("No se pudo crear la sesión de reminiscencia")
            return render(request, "Cuidador/inicioCuidador.html",{"exito":'true', 'name': decodedToken['first_name'], 'access':token})
        else:
            reminiscencia = Ap_Reminiscencia.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy)
            reminiscencia.save()
            print(clave)
            return render(request, "Cuidador/inicioCuidador.html",{"clave":clave, 'name': decodedToken['first_name'], 'access':token})
    return render(request, "Cuidador/inicioCuidador.html",{'name': decodedToken['first_name'], 'access':token})

def ingresarDatos (request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    userc = Cuidador.objects.filter(user_id=user)[0].id
    preguntas = []
    i = random.randint(1,79)
    #print(i)
    pregunta = Cat_Pregunta.objects.filter(idReactivo = i)
    preguntas.append(pregunta[0])
     
    if request.method == 'POST':
        #print("entro post")
        #andamos viedno como hacer funcionar la parte de ingresar datos con el nuevo modelo de usuarios
        idC = Cuidador.objects.get(id = userc)
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
    return render(request, "Cuidador/ingresarDatos.html",{'preguntas':preguntas, 'access':token})

