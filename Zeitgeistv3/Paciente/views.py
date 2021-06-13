from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from Cuidador.models import Pregunta, Cat_Pregunta
from .models import Paciente, Ap_Reminiscencia, Reminiscencia, Ap_Screening, Screening, Tema, Palabra, Ent_Cogn
from .forms import FormEditarP
from .aws import get_transcription
from Usuario.models import Paciente
from Usuario.apiviews import PacienteUser
from word_search_puzzle.utils import display_panel
from word_search_puzzle.algorithms import create_panel
import random
import requests
import json
import jwt
import datetime
import string
import numpy as np
import threading

#diccionario para guardar la respuestas de transcribe y analizarlas al terminar la prueba
respuestasT= {}

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


def inicioPa(request):
    try:
        return render(request, "Paciente/inicioPaciente.html")
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html")


def rmsc1(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    userp = Paciente.objects.filter(user_id=user)[0].id
    if request.method == "POST":
        cve = request.POST['cveRem']
        if Ap_Reminiscencia.objects.filter(cveAcceso=cve, resultadoFinal__isnull=True):
            answers = []
            idR = []
            op = {}  # {"1":[Ana, Mariana, Luisa], "84": [5,8,9]}
            img = {}  # {"5" : "/reminiscencia/sala.jgp", ...}
            audio = {}
            cuidador = Paciente.objects.get(id=userp).cuidador_id
            preguntas = Pregunta.objects.filter(idCuidador_id=cuidador)
            for item in preguntas:
                idR.append(item.idReactivo.idReactivo)
            random.shuffle(idR)
            j = 0
            for pregunta in preguntas:
                for i in idR[0:10]:
                    if i == pregunta.idReactivo.idReactivo:
                        j += 1
                        print("{cont}: i = {idr}, pregunta = {p}".format(cont=j, idr=i, p =pregunta.idReactivo_id))
                        answers.append(pregunta.idReactivo)
                        if pregunta.idReactivo.tipoPregunta == 'OP':op[pregunta.idReactivo.idReactivo] = pregunta.respuestaCuidador.split("-")[1::]
                        if pregunta.imagen:
                            img[pregunta.idReactivo.idReactivo] = pregunta.imagen
                        if pregunta.audio:
                            audio[pregunta.idReactivo.idReactivo] = pregunta.audio
            print(answers)
            return render(request, "Paciente/reminiscencia1.html", {"cve": cve, "preguntas": answers, "op": op, "img": img, "audio": audio, 'access': token, 'tipo': tipo, 'name': decodedToken['first_name']})
        else:
            return render(request, "Paciente/inicioPaciente.html", {'response': 'novalid', 'name': decodedToken['first_name'], 'access': token,  'tipo': tipo})


def saveAnswer(request):
    if request.is_ajax():
        print("entro ajax")
        cve = Ap_Reminiscencia.objects.filter(
            cveAcceso=request.POST.get('txtCve'))[0]
        idR = request.POST.get('txtidReactivo')
        idRe = Pregunta.objects.filter(idReactivo=idR)[0]
        pk = request.POST.get('txtCve')+idR
        respCorrecta = normalize(Pregunta.objects.filter(
            idReactivo=idR)[0].respuestaCuidador.lower())
        val = False
        if Cat_Pregunta.objects.filter(idReactivo=idR)[0].tipoPregunta == 'A':
            respuesta = normalize(request.POST.get('txtrespuestaA').lower())
            print("respuesta del paciente", respuesta)
            respCorrecta = respCorrecta.split(" ")
            print("respuesta correcta: ", respCorrecta)
            for word in respCorrecta:
                print(word)
                if respuesta.find(word) != -1:
                    print(respuesta.find(word))
                    val = True
                    break
        else:
            respuesta = request.POST.get('respuestaOP')
            respCorrecta = respCorrecta.split("-")[int(respCorrecta[0])]
            if respuesta.lower() == respCorrecta.lower():
                val = True
        print(val)
        try:
            registro = Reminiscencia.objects.create(
                idApp=pk, cveAcceso=cve, idPregunta=idRe, respuestaPaciente=respuesta, valoracion=val)
            registro.save()
            mensaje = f'respuesta registrada correctamente'
            error = 'No hay error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 201
            return response
        except:
            print("No se pudo realizar el registro")
            mensaje = f'no se pudo realizar el registro'
            error = 'Hay un error'
            response = JsonResponse({'mensaje': mensaje, 'error': error})
            response.status_code = 400
            return response
    else:
        print("no entro ajax")
        return redirect("/paciente")


def setCalif(request, clave, token, tipo):
    decodedToken = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=['HS256'])
    idR = Ap_Reminiscencia.objects.filter(cveAcceso=clave)[0]
    respuestas = Reminiscencia.objects.filter(
        cveAcceso=idR, valoracion=True).count()
    idR.resultadoFinal = respuestas
    idR.save()
    return render(request, "Paciente/inicioPaciente.html", {'name': decodedToken['first_name'], 'access': token, 'tipo': tipo})


# estan quedando pendiente para revision del doctor el reloj, lugar y localidad

def moca(request, token, tipo):
    decodedToken = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=['HS256'])
    iduser = decodedToken['user_id']
    pacient = Paciente.objects.filter(user_id=iduser)[0]
    print(pacient)
    if request.method == "POST":
        cve = request.POST.get('cveSc')
        if Ap_Screening.objects.filter(cveAcceso=cve, resultadoFinal__isnull=True, paciente_id=pacient):
            return render(request, "Paciente/tamizaje1.html", {"access": token, "cve": cve, 'tipo': tipo, 'name': decodedToken['first_name'], 'user': iduser})
        else:
            print("que esta pasando aqui?")
            return render(request, "Paciente/inicioPaciente.html", {'name': decodedToken['first_name'], "access": token, 'tipo': tipo})

#realiza el registro en la base de datos de las respuestas de cada reactivo del moca
def makeregistermoca(cve, idR, respuesta, resultado, pmax):
    sc = Ap_Screening.objects.filter(cveAcceso=cve)[0]
    #try:
    print(resultado)
    if idR == 2 or idR == 3:
        registro = Screening.objects.create(idApp=cve+str(idR), cveAcceso=sc, idReactivo=idR,
                                        respuestaImg=respuesta, puntajeReactivo=resultado, puntajeMaximo=pmax)
    else:
        if idR == 5:
            resultado = 0
        registro = Screening.objects.create(idApp=cve+str(idR), cveAcceso=sc, idReactivo=idR,
                                        respuestaT=respuesta, puntajeReactivo=resultado, puntajeMaximo=pmax)
    registro.save()
    mensaje = f'respuesta registrada correctamente'
    error = 'No hay error'
    response = JsonResponse({'mensaje': mensaje, 'error': error})
    response.status_code = 201
    return response
    #except:
        # print("No se pudo realizar el registro")
        # mensaje = f'no se pudo realizar el registro'
        # error = 'Hay un error'
        # response = JsonResponse({'mensaje': mensaje, 'error': error})
        # response.status_code = 400
        # return response


def basetranscript(clave, reactivo, cadena):
    response = {}
    name = clave+reactivo
    audio_name = clave+reactivo+".ogg"
    transcript = normalize(get_transcription(name, audio_name)).lower().replace(" ","").replace(".", "").replace(",", "")
    response["transcript"] = transcript
    resultado = 0
    if transcript != "Falló el transcript":
        if transcript != None:
            print(transcript)
            if reactivo == "101":
                if transcript == cadena or transcript == "solosequeletocajuanayudarhoy":
                    resultado = 1
                    print("se ganó el punto")
                else:
                    print("no lo hizo bien")
            else:
                if transcript == cadena:
                    resultado = 1
                    print("se ganó el punto")
                else:
                    print("no lo hizo bien")
        else:
            print("Transcripción vacía")
    else:
        print("Falló el transcript")
    response["resultado"] = resultado
    print(response)
    return response


def moca1(request):
    if request.is_ajax():
        resultado = 0
        respuesta = request.POST.get('txtstring')
        cve = request.POST.get('txtCve')
        print("respuesta ", respuesta)
        if respuesta == "1A2B3C4D5E":
            resultado = 1
        return makeregistermoca(cve, 1, respuesta, resultado, 1)
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca2_3(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        objeto = request.POST.get('object')
        if objeto == 'cubo':
            react = 2
            pmax = 1
            img = request.FILES.get('imgcubo')
        else:
            react = 3
            pmax = 3
            img = request.FILES.get('imgreloj')
        return makeregistermoca(cve, react, img, 0, pmax)
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca4(request):
    if request.is_ajax():
        resultado = 0
        animal1 = normalize(request.POST.get(
            'animal1').lower().replace(" ", ""))
        animal2 = normalize(request.POST.get(
            'animal2').lower().replace(" ", ""))
        animal3 = normalize(request.POST.get(
            'animal3').lower().replace(" ", ""))
        respuesta = animal1+animal2+animal3
        cve = request.POST.get('txtCve')
        print("respuesta ", respuesta)
        if animal1 == "leon":
            resultado += 1
        if animal2 == "rinoceronte":
            resultado += 1
        if animal3 == "camello" or animal3 == "dromedario":
            resultado += 1
        return makeregistermoca(cve, 4, respuesta, resultado, 3)
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca5(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        respuestasT["5"] = {}
        respuestasT["5"]["cve"] = cve
        respuestasT["5"]["cadena"] = "rostrosedatemploclavelrojo"
        respuestasT["5"]["pMax"] = 0
        response = JsonResponse({'mensaje': "reactivo 5-1 y 5-2 guardado para evaluacion", 'error': 'No error'})
        response.status_code = 200
        return response
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca6(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        respuestasT["6"] = {}
        respuestasT["6"]["cve"] = cve
        respuestasT["6"]["cadena"] =  "dosunoochocincocuatro"
        respuestasT["6"]["pMax"] = 1
        response = JsonResponse({'mensaje': "reactivo 6 guardado para evaluacion", 'error': 'No error'})
        response.status_code = 200
        return response
    else:
        print("no entro ajax")
        return redirect("/paciente")


def moca7(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        respuestasT["7"] = {}
        respuestasT["7"]["cve"] = cve
        respuestasT["7"]["cadena"] =  "doscuatrosiete"
        respuestasT["7"]["pMax"] = 1
        response = JsonResponse({'mensaje': "reactivo 7 guardado para evaluacion", 'error': 'No error'})
        response.status_code = 200
        return response
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca8(request):
    if request.is_ajax():
        respuestas = ['03','06','07','10','12','14','15','15','17','20','21']
        resultado = 0
        i = 0
        fallas = 0
        minutos = []
        cve = request.POST.get('txtCve')
        respuesta = request.POST.get('timespush')
        tiempos = respuesta.split('/')
        if len(tiempos) < 13:
            for time in tiempos:
                if len(time) > 0:
                    minutos.append(time.split(" ")[1])
            for minut in minutos:
                if minut != respuestas[i]:
                    if i != 2:
                        fallas += 1
                i+=1
            if fallas < 2: 
                resultado = 1
        return makeregistermoca(cve, 8, respuesta, resultado, 1)
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca9(request):
    if request.is_ajax():
        num = 100
        nums = []
        resultado = 0
        cuenta = 0
        respuesta = ""
        for i in range(0, 5):
            nums.append(request.POST.get('numero'+str(i+1)+'').replace(" ", ""))
        cve = request.POST.get('txtCve')
        for i in range(0, 5):
            num -= 7
            if int(nums[i]) == num:
                cuenta += 1
            respuesta += str(nums[i])
        if cuenta == 4 or cuenta == 5:
            resultado = 3
        elif cuenta == 3 or cuenta == 2:
            resultado = 2
        elif cuenta == 1:
            resultado = 1
        return makeregistermoca(cve, 9, respuesta, resultado, 3)
    else:
        print("no entro ajax")
        return redirect("/paciente")


def moca10(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        respuestasT["10"] = {}
        respuestasT["10"]["cve"] = cve
        respuestasT["10"]["cadena"] = "solosequeletocaajuanayudarhoy-elgatosiempreseescondedebajodelsofacuandohayperrosenlahabitacion"
        respuestasT["10"]["pMax"] = 2
        response = JsonResponse({'mensaje': "reactivo 10-1 y 10-2 guardado para evaluacion", 'error': 'No error'})
        response.status_code = 200
        return response
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca11(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        respuestasT["11"] = {}
        respuestasT["11"]["cve"] = cve
        respuestasT["11"]["pMax"] = 1
        response = JsonResponse({'mensaje': "reactivo 11 guardado para evaluacion", 'error': 'No error'})
        response.status_code = 200
        return response
    else:
        print("no entro ajax")
        return redirect("/paciente")
        
def moca12(request):
    if request.is_ajax():
        resultado = 0
        cat2 = normalize(request.POST.get('categoria2').lower().replace(" ", ""))
        cat3 = normalize(request.POST.get('categoria3').lower().replace(" ", ""))
        respuesta = cat2+cat3
        cve = request.POST.get('txtCve')
        if cat2.find("transporte") != -1:
            resultado += 1
        if cat3.find("medi") != -1 or cat3.find("herramienta") != -1:
            resultado += 1
        return makeregistermoca(cve, 12, respuesta, resultado, 2)
    else:
        print("No entro ajax")
        return redirect("/paciente")


def moca13(request):
    if request.is_ajax():
        resultado = 0
        correctas = ['rostro', 'templo', 'clavel', 'rojo', 'seda']
        puntos = []
        respuesta = " "
        for i in range(0, 5):
            puntos.append(int(request.POST.get('resultadop'+str(i+1)+'')))
            respuesta += normalize(request.POST.get('palabra'+str(i+1)+'').lower().replace(" ", ""))
        cve = request.POST.get('txtCve')
        for i in range(0, len(correctas)):
            if respuesta.find(correctas[i]):
                resultado += 3 - puntos[i]
        return makeregistermoca(cve, 13, respuesta, resultado, 15)
    else:
        print("No entro ajax")
        return redirect("/paciente")


def moca14(request):
    weekday = {
        'lunes': 0,
        'martes': 1,
        'miercoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sabado': 5,
        'domingo': 6,
    }

    month = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12,
    }
    if request.is_ajax():
        resultado = 0
        respuesta = ""
        diasemana = weekday.get(normalize(request.POST.get('diasemana').lower().replace(" ", "")))
        dia = normalize(request.POST.get('dia').lower().replace(" ", ""))
        mes = month.get(normalize(request.POST.get('mes').lower().replace(" ", "")))
        anio = normalize(request.POST.get('anio').lower().replace(" ", ""))
        lugar = normalize(request.POST.get('lugar').lower().replace(" ", ""))
        localidad = normalize(request.POST.get('localidad').lower().replace(" ", ""))

        cve = request.POST.get('txtCve')
        fecha = date.today()
        if diasemana == fecha.weekday():
            resultado += 1
            respuesta += "1"
        else:
            respuesta += "0"
        if int(dia) == fecha.day:
            resultado += 1
            respuesta += "-1"
        else:
            respuesta += "-0"
        if mes == fecha.month:
            resultado += 1
            respuesta += "-1"
        else:
            respuesta += "-0"
        if int(anio) == fecha.year:
            resultado += 1
            respuesta += "-1"
        else:
            respuesta += "-0"
        respuesta +="-"+lugar+"-"+localidad
        return makeregistermoca(cve, 14, respuesta, resultado, 6)
    else:
        print("No entro ajax")
        return redirect("/paciente")


#Hacer todo el proceso de todos los reactivos que usen transcribe al terminar la prueba para que no tarde en cada reactivo
def calificarTranscribe():
    for reactivo in respuestasT.keys():
        print(reactivo)
        if reactivo == "11":
            resultado = 0
            palabras =  0 
            name = respuestasT[reactivo]["cve"] + "11"
            audio_name = respuestasT[reactivo]["cve"]+"11.ogg"
            transcript = normalize(get_transcription(name, audio_name)).lower().replace(".", "").replace(",", "").split(" ")
            sinduplicados = list(set(transcript))
            print(sinduplicados)
            for word in sinduplicados:
                if len(word) > 0:
                    if word[0] == 'f':
                        palabras += 1
            if palabras >= 11:
                resultado = 1
        else:
            if reactivo == "10" or reactivo=="5":
                if reactivo=="10":
                    cad1 = respuestasT[reactivo]["cadena"].split("-")[0]
                    cad2 = respuestasT[reactivo]["cadena"].split("-")[1]
                else:
                    cad1 = respuestasT[reactivo]["cadena"]
                    cad2 = respuestasT[reactivo]["cadena"]
                print("cadena1: ",cad1)
                print("cadena2: ",cad2)
                respuesta = basetranscript(respuestasT[reactivo]["cve"], reactivo+"1", cad1)
                transcript = respuesta["transcript"]
                resultado = respuesta["resultado"]
                respuesta2 = basetranscript(respuestasT[reactivo]["cve"], reactivo+"2", cad2)
                transcript += "-"+respuesta2["transcript"]
                resultado += respuesta2["resultado"]
            else:
                respuesta = basetranscript(respuestasT[reactivo]["cve"], reactivo, respuestasT[reactivo]["cadena"])
                transcript = respuesta["transcript"]
                resultado = respuesta["resultado"]            
        response = makeregistermoca(respuestasT[reactivo]["cve"], reactivo, transcript, resultado, respuestasT[reactivo]["pMax"])
        print(response)
    idT = Ap_Screening.objects.filter(cveAcceso=respuestasT["7"]["cve"])[0]
    idT.resultadoFinal = 41 #41 significa que ya acabó de hacerla pero aun no se hace la cuenta completa de todos los reactivos
    idT.save()
    print("se han calificado las respuestas de transcribe")


def finalizarmoca(request, token, tipo):
    decodedToken = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=['HS256'])
    thread = threading.Thread(target=calificarTranscribe)
    thread.start()
    return render(request, "Paciente/inicioPaciente.html", {'name': decodedToken['first_name'], 'access':token, 'tipo':tipo, 'nota':'terminadomoca'})


def enterEntCogn(request, token, tipo):
    decodedToken = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=['HS256'])
    if request.method =="POST":
        cve = request.POST['cveRem']
        if Ent_Cogn.objects.filter(cveAcceso=cve, estado='NS'):
            return render(request, "Paciente/entCognitivo.html", {'access': token, 'cve':cve, 'tipo':tipo, 'name': decodedToken['first_name']})
        else:
            return render(request, "Paciente/inicioPaciente.html", {'response':'novalid', 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})

def entCog(request, token, tipo):
    decodedToken = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    pacient = Paciente.objects.filter(user_id=user)[0].id
    if request.method == 'POST':
        dificultad = request.POST.get('nivel')
        palabras = []
        tiempo = request.POST.get('tiempo')
        clave = request.POST.get('cve')
        print(clave)
        if dificultad != None:
            try:
                if dificultad == 'F':
                    N = 8
                    p = 6
                elif dificultad == 'M':
                    N = 10
                    p = 9
                else:
                    N = 12
                    p = 12
                palabrasDB = []
                cveP = []
                t = Tema.objects.filter(dificultad=dificultad)
                """if len(t) == 1:
                    nivel = 0
                else:
                    nivel = random.randint(0,len(t)-1)"""
                nivel = random.randint(0, len(t)-1)
                # print(t)
                # print(nivel)
                tema = t[nivel].cveTemas
                print("tema")
                print(tema)
                palabrasDB = Palabra.objects.filter(tema= tema)
                for palabra in palabrasDB:
                    cveP.append(palabra.cvePalabra)

                random.shuffle(cveP)

                for i in cveP[0:p]:
                    for palabra in palabrasDB:
                        if i == palabra.cvePalabra:
                            palabras.append(palabra.palabra)

                ## Sopa (matriz)##
                result = create_panel(
                    height=N, width=N, words_value_list=palabras)
                mat = []
                sopa = [None] * N
                for i in range(0, N):
                    sopa[i] = [None] * N

                sopa = result.get('panel').cells
                for key in sopa:
                    #print (key,":",sopa[key])
                    mat.append(sopa[key].upper())

                mat = np.asarray(mat)
                mat = np.resize(mat, (N,N))
                return render(request, "Paciente/entCognitivo.html", {'access': token, "palabras":palabras, "mat":mat, "tema":tema, 'clave':clave, 'tipo':tipo, 'name': decodedToken['first_name']})
            except:
                print("Ocurrió un error. Sopa")
                return render(request, "Paciente/entCognitivo.html", {'access': token, 'tipo':tipo, 'name': decodedToken['first_name']})

        elif tiempo != None:
            claveA = request.POST.get('cveA')
            if Ent_Cogn.objects.filter(cveAcceso=claveA, estado='NS'):
                ap_sopa = Ent_Cogn.objects.get(cveAcceso=claveA)
                print(claveA)
                print(ap_sopa)
                print(pacient)
                fecha = datetime.datetime.today()
                fecha = str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
                print(fecha)
                ct = Tema()
                ct.cveTemas = request.POST.get('ct')
                ap_sopa.cveTema_id = ct
                ap_sopa.paciente_id = pacient
                ap_sopa.fechaAp = fecha
                ap_sopa.estado = 'S'
                ap_sopa.tiempo = tiempo
                ap_sopa.save()
                print("Guardado")

                return render(request, "Paciente/inicioPaciente.html", {'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})

            else:
                print("Ocurrió un error.")
                return render(request, "Paciente/entCognitivo.html", {'access': token, 'tipo':tipo, 'name': decodedToken['first_name']})
    else:
        return render(request, "Paciente/entCognitivo.html", {'access': token, 'tipo':tipo, 'name': decodedToken['first_name']})


def editP(request, token, tipo, name):
    try:
        base = "Paciente/basePacientes.html"  # Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        decodedToken = jwt.decode(
            token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        print("iduser", iduser)
        infoU = requests.get('http://52.36.58.133/v1/userd/'+str(iduser)+'')
        infoP = requests.get(
            'http://52.36.58.133/v1/Pacienteuser/'+str(iduser)+'')
        if infoP.ok and infoU.ok:
            initial_dict = {
                "nvo_nombre": json.loads(infoU.content)['first_name'],
                "nvo_apellidos": json.loads(infoU.content)['last_name'],
                "nvo_nombreUsuario":json.loads(infoU.content)['username'],
                "nvo_correo":json.loads(infoU.content)['email'],
                "nvo_sexo":json.loads(infoP.content)['sexo'],
                "nvo_escolaridad":json.loads(infoP.content)['escolaridad'],
                "nvo_fechaDiag":json.loads(infoP.content)['fechaDiag']
            }
        else:
            print("Ocurrio error en usuario ", infoU.status_code)
            print("Ocurrio error en paciente ", infoP.status_code)
        if request.method =="POST": 
            feditP = FormEditarP(request.POST, initial=initial_dict)
            # try:
            if feditP.is_valid():
                fechaDiag = feditP.cleaned_data['nvo_fechaDiag']  # necesitamos que la fecha sea STR para hacer las operaciones de conversión a JSON
                fechaDiag_str = str(fechaDiag)
                fecha = datetime.date.today()

                if fechaDiag > fecha or fechaDiag.year < 1950:
                    return render(request, "Paciente/editarPaciente.html", {"name": feditP.cleaned_data['nvo_nombre'], "form": feditP, "tipo": tipo, "user": iduser, "access": token, "problema_fechaDiag" : True, "base": base})

                payload = {
                    "username": feditP.cleaned_data['nvo_nombreUsuario'],
                    "first_name": feditP.cleaned_data['nvo_nombre'],
                    "last_name": feditP.cleaned_data['nvo_apellidos'],
                    "email": feditP.cleaned_data['nvo_correo']
                }
                updateU = requests.put('http://52.36.58.133/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
                            payload), headers={'content-type': 'application/json', "Authorization": "Bearer " + token +""})
                if updateU.ok:
                    print("Se pudo actualizar el usuario")
                    payloadP = {
                        "sexo":feditP.cleaned_data['nvo_sexo'],
                        "escolaridad":feditP.cleaned_data['nvo_escolaridad'],
                        "fechaDiag": fechaDiag_str,
                        "cuidador":json.loads(infoP.content)['cuidador'],
                        "especialista":json.loads(infoP.content)['especialista'],
                    }
                    print(payloadP)
                    updateP = requests.put('http://52.36.58.133/v1/editarpaciente/'+str(json.loads(infoP.content)['id']) + '', data=json.dumps(payloadP), headers={'content-type': 'application/json'})
                    if updateP.ok:
                        return render(request, "Paciente/inicioPaciente.html", {"name": feditP.cleaned_data['nvo_nombre'], "tipo": tipo, "access": token, "modified" : True})
                    else:
                        print(updateP.json())
                else:
                    print(updateU.json())
                    print("No se pudo hacer el registro del usuario")
                    return render(request, "Paciente/editarPaciente.html", {"name": feditP.cleaned_data['nvo_nombre'], "form": feditP, "tipo": tipo, "user": iduser, "access": token, "already_exists": True, "base": base})

        else:
            feditP = FormEditarP(initial=initial_dict)
        return render(request, "Paciente/editarPaciente.html", {"name": name, "form": feditP, "tipo": tipo, "user": iduser, "base": base, "access": token})  # Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html")        

def get_prom(dificultad, tiempo):
    if dificultad == 'F':
        time = tiempo
        segundos = time.second+time.minute*60+time.hour*3600
        n = round(segundos / 6, 2)
    elif dificultad == 'M':
        time = tiempo
        segundos = time.second+time.minute*60+time.hour*3600
        n = round(segundos / 9, 2)
    else:
        time = tiempo
        segundos = time.second+time.minute*60+time.hour*3600
        n = round(segundos / 12,2)
    return n    

def reportes(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']    
    paciente = Paciente.objects.filter(user_id=user)[0].id
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
    
    return render(request, "Paciente/reportes.html",{"pruebas":pruebas, "sopas":sopas,"reminiscencia":reminiscencia,"graficaS":graS, 'graficaR': graR, 'name': decodedToken['first_name'], 'access':token, 'tipo':tipo})
