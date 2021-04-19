from django.shortcuts import render
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import authentication_classes, permission_classes
from Cuidador.permissions import IsOwnerOrReadOnly
from .models import Cuidador, Pregunta, Cat_Pregunta
from Pruebas.models import Reminiscencia, Ap_Reminiscencia, Paciente
from .serializers import CuidadorSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from .forms import FormDatosImg
import random
import datetime
import string

nomusu = 'atziri99'
pacient = Paciente.objects.filter(cuidador=nomusu)[0]

def inicioC(request):
    return render(request, "Cuidador/inicioCuidador.html", {'user': nomusu})

def editC(request):
    return render(request, "Cuidador/editarCuidador.html")

def getcveAcceso(request):
    ckey = Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True, paciente=pacient)[0].cveAcceso
    return render(request, "Cuidador/inicioCuidador.html")

def cveAcceso(request):
    fecha = datetime.datetime.now()
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
        return render(request, "Cuidador/inicioCuidador.html",{"clave":clave})
    return render(request, "Cuidador/inicioCuidador.html")


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
        print("entro post")
        idC = Cuidador.objects.get(nomUsuario=nomusu)
        idReact = Cat_Pregunta()
        idReact.idReactivo= request.POST.get('idR')
        pregunta = Pregunta()
        pregunta.idReactivo = idReact
        pregunta.idCuidador = idC
        pregunta.imagen = request.FILES.get('img')
        pregunta.audio = request.FILES.get('aud')
        pregunta.respuestaCuidador = request.POST.get('respuesta')

        try:
            pregunta.save()
            print("Guardado")
        except:
            print("Error")
   
    return render(request, "Cuidador/IngresarDatosCuidador.html",{'preguntas':preguntas})
    #necesitamos idCuidador y idReactivo
    # preguntaL = []
    # formL = []
    # preguntas = Cat_Pregunta.objects.filter(tipoDato="IMG")
    # print(len(preguntas))
    # for pregunta in preguntas:
    #     form = FormDatosImg()
    #     print(request.method)
    #     if request.method == 'POST':
    #         print("entro post")
    #         form = FormDatosImg(request.POST, request.FILES)
    #         if form.is_valid():                
    #             idR = pregunta.idReactivo
    #             print(idR)
    #             idC = Cuidador(nomUsuario='atziri99')
    #             respuesta = form.cleaned_data['respuesta']
    #             img = form.cleaned_data['imagen']
    #             pregunta = Pregunta.objects.create(idReactivo= idR, idCuidador=idC, imagen=img, respuestaCuidador = respuesta)
    #             pregunta.save()
    #             preguntaL.append(pregunta.reactivo)
    #             formL.append(form)
    #             return render(request, "Cuidador/IngresarDatosCuidador.html", {'preguntas': preguntaL , 'forms': formL})

    #     else:
    #         form = FormDatosImg()
    # return render(request, "Cuidador/IngresarDatosCuidador.html", {'preguntas': preguntaL , 'forms': formL})

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


class CuidadorList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CuidadorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer