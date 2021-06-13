from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import Pregunta, Cat_Pregunta
from django.conf import settings
from Usuario.models import Cuidador, Paciente
from Paciente.models import Reminiscencia, Ap_Reminiscencia, Ent_Cogn
from Paciente.views import get_prom
from django.contrib.auth.models import User
from rest_framework import permissions
from Usuario import views
from Especialista.models import Mensaje
from .forms import FormDatosImg, FormEditarC
import random, datetime, string, re, json, jwt, requests

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


 
def inicioC(request, token, tipo):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        return render(request, "Cuidador/inicioCuidador.html",{'tipo': tipo,'name': decodedToken['first_name'], 'access':token})
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html")


def editC(request, token, tipo, name):
    try:   
        base = "Cuidador/baseCuidador.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        print("iduser", iduser)
        infoU = requests.get('http://52.36.58.133/v1/userd/'+str(iduser)+'')
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
                updateU =  requests.put('http://52.36.58.133/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
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

def getcveAcceso(request, token, treatment, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    userc = Cuidador.objects.filter(user_id=user)[0]
    if  Pregunta.objects.filter(idCuidador_id=userc).count() < 10:
        return render(request, "Cuidador/inicioCuidador.html",{"noanswers": 'true', 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
    else:
        pacient = Paciente.objects.filter(cuidador=userc)[0]
        if treatment == 'rem':
            ckey = Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True, paciente=pacient)[0].cveAcceso
            prueba = 'reminiscencia'
        elif treatment == "entcogn":
            ckey = Ent_Cogn.objects.filter(estado='NS', paciente=pacient)[0].cveAcceso
            prueba = 'entrenamiento cognitivo'
        return render(request, "Cuidador/inicioCuidador.html",{"clave":ckey, "prueba":prueba, 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})

def cveAcceso(request, token, treatment, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    userc = Cuidador.objects.filter(user_id=user)[0]
    if  Pregunta.objects.filter(idCuidador_id=userc).count() < 10 and treatment == 'rem':
        return render(request, "Cuidador/inicioCuidador.html",{"noanswers": 'true', 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
    else:
        pacient = Paciente.objects.filter(cuidador=userc)[0] #ide del paciente relacionado con el cuidador
        fecha = datetime.datetime.now()
        fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
        clave = str(fecha.day)+str(fecha.month)+str(fecha.year)[2:4]+str(fecha.hour)+str(fecha.minute)+str(user)+random.choice(string.ascii_uppercase)+str(random.randint(0,9))+random.choice(string.ascii_uppercase)
        if treatment == 'rem':
            prueba = 'reminiscencia' 
            if Ap_Reminiscencia.objects.filter(resultadoFinal__isnull=True ,paciente=pacient): 
                print("No se pudo crear la sesión de reminiscencia")
                return render(request, "Cuidador/inicioCuidador.html",{'prueba': prueba, "exito":'true', 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
            else:
                reminiscencia = Ap_Reminiscencia.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy)
                reminiscencia.save()
                print(clave)
                return render(request, "Cuidador/inicioCuidador.html",{'prueba': prueba, "clave":clave, 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
        elif treatment == "entcogn":
            prueba = 'entrenamiento cognitivo'
            if Ent_Cogn.objects.filter(estado='NS' ,paciente=pacient): 
                print("No se pudo crear la sesión de sopa de letras")
                return render(request, "Cuidador/inicioCuidador.html",{'prueba':prueba, "exito":'true', 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
            else:
                sopadeletras = Ent_Cogn.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy, estado='NS')
                sopadeletras.save()
                print(clave)
                return render(request, "Cuidador/inicioCuidador.html",{'prueba':prueba, "clave":clave, 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
    return render(request, "Cuidador/inicioCuidador.html",{'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})

def ingresarDatos (request, token, tipo):
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
    return render(request, "Cuidador/ingresarDatos.html",{'preguntas':preguntas, 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})


def verMensajes(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    idUser = decodedToken['user_id']
    id_Cuidador = Cuidador.objects.filter(user_id=idUser)[0]
    lista_msg_final = {}

    mensajes = Mensaje.objects.filter(cuidador=id_Cuidador)
    mensajesList = list(mensajes.values())

    if not mensajes.exists(): #Si el cuidador no tiene mensajes, lo notificamos.
        return render(request, "Cuidador/verMensajes.html", {'No_tiene_mensajes': True, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, "base": "Especialista/baseEspecialista.html"})
    else:
        for msg in mensajesList: #Generamos diccionario e iremos guardando los datos importantes del mensaje
            lista_msg_final[msg['cveMensaje']] = msg
            lista_msg_final[msg['cveMensaje']]['fechaEnvio'] = msg['fechaEnvio'].strftime('%d / %m / %Y')
        return render(request, "Cuidador/verMensajes.html", {'listMessages': lista_msg_final, 'access':token, 'name':decodedToken['first_name'], 'tipo':tipo})


def eliminarMensaje(request, token, tipo, msg_e):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    idUser = decodedToken['user_id']
    id_Cuidador = Cuidador.objects.filter(user_id=idUser)[0]
    lista_msg_final = {}

    mensaje = Mensaje.objects.get(cveMensaje=msg_e)
    mensaje.delete()
    mensajes = Mensaje.objects.filter(cuidador=id_Cuidador)
    mensajesList = list(mensajes.values())

    if not mensajes.exists(): #Si el cuidador no tiene mensajes, lo notificamos.
        return render(request, "Cuidador/verMensajes.html", {'No_tiene_mensajes': True, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, "base": "Especialista/baseEspecialista.html", 'success_dmsg': True})
    else:
        for msg in mensajesList: #Generamos diccionario e iremos guardando los datos importantes del mensaje
            lista_msg_final[msg['cveMensaje']] = msg
            lista_msg_final[msg['cveMensaje']]['fechaEnvio'] = msg['fechaEnvio'].strftime('%d / %m / %Y')
        return render(request, "Cuidador/verMensajes.html", {'listMessages': lista_msg_final, 'access':token, 'name':decodedToken['first_name'], 'tipo':tipo, 'success_dmsg': True})


def reportesC(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    cuidador = decodedToken['user_id']
    userc = Cuidador.objects.filter(user_id=cuidador)[0].id
    paciente = Paciente.objects.filter(cuidador_id=userc)[0].id
    pruebas = []
    sopas = []
    longitud = len(Ent_Cogn.objects.filter(paciente=paciente))
    print(longitud)
    for i in range(0,longitud):        
        pruebas.append(Ent_Cogn.objects.filter(paciente=paciente)[i])
        prueba = Ent_Cogn.objects.filter(paciente=paciente)[i]
        if prueba.estado == 'S':
            promedio = get_prom(prueba.cveTema.dificultad, prueba.tiempo)
        else:
            promedio = 0
        sopa = {'datos': prueba, 'promedio': promedio}
        sopas.append(sopa)
    
    print(sopas)
    
    graS = []
    if longitud <= 5:
        for i in range(0,longitud):
            sdl = Ent_Cogn.objects.filter(paciente=paciente)[i]
            if sdl.estado == 'S':
                time = sdl.tiempo
                segundos = time.second+time.minute*60+time.hour*3600
                datoS = {'clave': sdl.cveAcceso , 'fecha':sdl.fechaAp, 'resultado': segundos }
                datoN = {'dificultad': sdl.cveTema.dificultad, 'datos': datoS, 'estado': sdl.estado}
                graS.append(datoN)
            else:
                datoS = {'clave': sdl.cveAcceso , 'fecha':sdl.fechaAp, 'resultado': 0 }
                datoN = {'dificultad': 'N', 'datos': datoS, 'estado': sdl.estado}
                graS.append(datoN)
            
    reminiscencia = []
    total = len(Ap_Reminiscencia.objects.filter(paciente=paciente))
    # Llenando para la tabla Reminiscencia
    if total == '0':
        reminiscencia.append('No ha realizado ninguna sesión de reminiscencia')
    else:
        for i in range(0,total):
            reminiscencia.append(Ap_Reminiscencia.objects.filter(paciente=paciente)[i])

    # Llenando para la gráfica
    graR = []
    if total <= 5:
        for i in range(0,total):
            rem = Ap_Reminiscencia.objects.filter(paciente=paciente)[i]
            datos = {'clave': rem.cveAcceso , 'fecha':rem.fechaAp, 'resultado': rem.resultadoFinal}
            graR.append(datos)
    else:
        for i in range(total-6,total):
            rem = Ap_Reminiscencia.objects.filter(paciente=paciente)[i]
            datos = {'clave': rem.cveAcceso , 'fecha':rem.fechaAp, 'resultado': rem.resultadoFinal}
            graR.append(datos)
    
    return render(request, "Cuidador/reportes.html",{"pruebas":pruebas, "sopas":sopas,"reminiscencia":reminiscencia,"graficaS":graS, 'graficaR': graR,  'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
