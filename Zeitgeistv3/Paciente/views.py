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
    decodedToken = jwt.decode(
        token, key=settings.SECRET_KEY, algorithms=['HS256'])
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
            for i in idR[0:10]:
                for pregunta in preguntas:
                    if i == pregunta.idReactivo.idReactivo:
                        answers.append(pregunta.idReactivo)
                        if pregunta.idReactivo.tipoPregunta == 'OP':
                            op[pregunta.idReactivo.idReactivo] = pregunta.respuestaCuidador.split(
                                "-")[1::]
                        if pregunta.imagen:
                            img[pregunta.idReactivo.idReactivo] = pregunta.imagen
                        if pregunta.audio:
                            audio[pregunta.idReactivo.idReactivo] = pregunta.audio
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
    try:
        print(resultado)
        if idR == 2:
            registro = Screening.objects.create(idApp=cve+str(idR), cveAcceso=sc, idReactivo=idR,
                                            respuestaImg=respuesta, puntajeReactivo=resultado, puntajeMaximo=pmax)
        else:
            registro = Screening.objects.create(idApp=cve+str(idR), cveAcceso=sc, idReactivo=idR,
                                            respuestaT=respuesta, puntajeReactivo=resultado, puntajeMaximo=pmax)
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


def basetranscript(clave, reactivo, cadena):
    response = {}
    name = clave+reactivo
    audio_name = clave+reactivo+".ogg"
    transcript = normalize(get_transcription(name, audio_name)).lower().replace(" ", "").replace(".", "").replace(",", "")
    response["transcript"] = transcript
    resultado = 0
    if transcript != None:
        print(transcript)
        if transcript == cadena:
            resultado = 1
            print("se ganó el punto")
        else:
            print("no lo hizo bien")
    else:
        print("hubo un error en la transcripción")
    response["resultado"] = resultado
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

def moca2(request):
    if request.is_ajax():
        cve = request.POST.get('txtCve')
        img = request.FILES.get('imgcubo')
        return makeregistermoca(cve, 2, img, 1, 1)
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
        if animal2 == "hipopotamo":
            resultado += 1
        if animal3 == "camello" or animal3 == "dromedario":
            resultado += 1
        return makeregistermoca(cve, 4, respuesta, resultado, 3)
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
        if cat2.find("transporte"):
            resultado += 1
        if cat3.find("medi") or cat3.find("herramienta"):
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
        diasemana = weekday.get(normalize(request.POST.get('diasemana').lower().replace(" ", "")))
        dia = normalize(request.POST.get('dia').lower().replace(" ", ""))
        mes = month.get(normalize(request.POST.get('mes').lower().replace(" ", "")))
        anio = normalize(request.POST.get('anio').lower().replace(" ", ""))
        lugar = normalize(request.POST.get('lugar').lower().replace(" ", ""))
        localidad = normalize(request.POST.get('localidad').lower().replace(" ", ""))

        respuesta = str(diasemana)+'-'+dia+'-'+str(mes)+ \
                        '-'+anio+'-'+lugar+'-'+localidad
        cve = request.POST.get('txtCve')
        fecha = date.today()
        if diasemana == fecha.weekday():
            resultado += 1
        if int(dia) == fecha.day:
            resultado += 1
        if mes == fecha.month:
            resultado += 1
        if int(anio) == fecha.year:
            resultado += 1
        return makeregistermoca(cve, 14, respuesta, resultado, 6)
    else:
        print("No entro ajax")
        return redirect("/paciente")



#Hacer todo el proceso de todos los reactivos que usen transcribe al terminar la prueba para que no tarde en cada reactivo
def calificarTranscribe():
    for reactivo in respuestasT.keys():
        if reactivo == "11":
            resultado = 0
            palabras =  0 
            name = reactivo.clave + "11"
            audio_name = reactivo.clave+"11.ogg"
            transcript = normalize(get_transcription(name, audio_name)).lower().replace(".", " ").replace(",", " ").split(" ")
            sinduplicados = list(set(transcript))
            for word in sinduplicados:
                if len(word) > 0:
                    if word[0] == 'f':
                        palabras += 1
            if palabras >= 11:
                resultado = 1
        else:
            if reactivo == "10":
                cad = reactivo.cadena.split("-")
                respuesta = basetranscript(reactivo.clave, "101", cad[0])
                transcript = respuesta["transcript"]
                resultado = respuesta["resultado"]
                respuesta2 = basetranscript(reactivo.clave, "102", cad[1])
                transcript += "-"+respuesta2["transcript"]
                resultado += respuesta2["resultado"]
            else:
                respuesta = basetranscript(reactivo.clave, reactivo, reactivo.cadena)
                transcript = respuesta["transcript"]
                resultado = respuesta["resultado"]            
        return makeregistermoca(reactivo.clave, reactivo, transcript, resultado, reactivo.pmax)


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
        #cve = '952112AMP'
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
        infoU = requests.get('http://127.0.0.1:8000/v1/userd/'+str(iduser)+'')
        infoP = requests.get(
            'http://127.0.0.1:8000/v1/Pacienteuser/'+str(iduser)+'')
        if infoP.ok and infoU.ok:
            initial_dict = {
                "nvo_nombre": json.loads(infoU.content)['first_name'],
                "nvo_apellidos": json.loads(infoU.content)['last_name'],
                "nvo_nombreUsuario": json.loads(infoU.content)['username'],
                "nvo_correo": json.loads(infoU.content)['email'],
                "nvo_sexo": json.loads(infoP.content)['sexo'],
                "nvo_escolaridad": json.loads(infoP.content)['escolaridad'],
                "nvo_fechaDiag": json.loads(infoP.content)['fechaDiag'] 
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
                updateU = requests.put('http://127.0.0.1:8000/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
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
                    updateP = requests.put('http://127.0.0.1:8000/v1/editarpaciente/'+str(json.loads(infoP.content)['id']) + '', data=json.dumps(payloadP), headers={'content-type': 'application/json'})
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
