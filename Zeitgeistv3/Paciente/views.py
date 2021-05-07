from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from datetime import datetime, date
from Cuidador.models import Pregunta, Cat_Pregunta
from .models import Paciente, Ap_Reminiscencia, Reminiscencia, Ap_Screening, Screening
from .forms import FormEditarP
from Usuario.models import Paciente
from Usuario.apiviews import PacienteUser
import random
import requests
import json
import jwt


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
    return render(request, "Paciente/inicioPaciente.html")
        
def rmsc1(request):
    if request.method=="POST":
        cve = request.POST['cveRem']
        if Ap_Reminiscencia.objects.filter(cveAcceso=cve, resultadoFinal__isnull=True):
            answers = []
            idR = []
            op= {} #{"1":[Ana, Mariana, Luisa], "84": [5,8,9]}
            img={} #{"5" : "/reminiscencia/sala.jgp", ...}
            audio = {}
            cuidador = Paciente.objects.get(nomUsuario='rosabermudez').cuidador.nomUsuario
            preguntas = Pregunta.objects.filter(idCuidador=cuidador)
            for item in preguntas:
                idR.append(item.idReactivo.idReactivo)
            random.shuffle(idR)
            for i in idR[0:10]:
                for pregunta in preguntas:
                    if i == pregunta.idReactivo.idReactivo:
                        answers.append(pregunta.idReactivo)
                        if pregunta.idReactivo.tipoPregunta == 'OP':
                            op[pregunta.idReactivo.idReactivo]= pregunta.respuestaCuidador.split("-")[1::]
                        if pregunta.imagen:
                            img[pregunta.idReactivo.idReactivo] = pregunta.imagen
                        if pregunta.audio:
                            audio[pregunta.idReactivo.idReactivo] = pregunta.audio
            return render(request, "Paciente/reminiscencia1.html", {"cve": cve,"preguntas":answers, "op":op, "img": img, "audio": audio})
        else:
            return redirect("/paciente/?novalid")

def saveAnswer(request):
    if request.is_ajax():
        print("entro ajax")
        cve = Ap_Reminiscencia.objects.filter(cveAcceso=request.POST.get('txtCve'))[0]
        idR = request.POST.get('txtidReactivo')
        idRe = Pregunta.objects.filter(idReactivo= idR)[0]
        pk = request.POST.get('txtCve')+idR
        respCorrecta = Pregunta.objects.filter(idReactivo=idR)[0].respuestaCuidador.lower()
        val = False
        if Cat_Pregunta.objects.filter(idReactivo=idR)[0].tipoPregunta == 'A':
            respuesta = request.POST.get('txtrespuestaA').lower()
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
            registro = Reminiscencia.objects.create(idApp = pk, cveAcceso= cve, idPregunta=idRe, respuestaPaciente=respuesta, valoracion= val)    
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

def setCalif(request, clave):
    idR = Ap_Reminiscencia.objects.filter(cveAcceso=clave)[0]
    respuestas = Reminiscencia.objects.filter(cveAcceso=idR, valoracion=True).count()
    idR.resultadoFinal = respuestas
    idR.save()
    return redirect("/paciente")


#estan quedando pendiente para revision del doctor el reloj, lugar y localidad

def moca(request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    iduser = decodedToken['user_id']
    pacient = Paciente.objects.filter(user_id=iduser)[0]
    print(pacient)
    if request.method=="POST":
        cve = request.POST.get('cveSc')
        if Ap_Screening.objects.filter(cveAcceso=cve, resultadoFinal__isnull=True, paciente_id=pacient):
            return render(request, "Paciente/tamizaje1.html", {"access": token, "cve":cve})
        else:
            print("que pedo que esta pasando aqui")
            return render(request, "Paciente/inicioPaciente.html", {"access": token})

def makeregistermoca(cve, idR, respuesta, resultado, pmax):
    sc = Ap_Screening.objects.filter(cveAcceso=cve)[0]
    try: 
        print(resultado)
        registro = Screening.objects.create(idApp=cve+str(idR), cveAcceso= sc, idReactivo=idR, respuestaT=respuesta, puntajeReactivo=resultado, puntajeMaximo=pmax)
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

def moca4(request):
    if request.is_ajax():
        resultado = 0
        animal1 = normalize(request.POST.get('animal1').lower().replace(" ", ""))
        animal2 = normalize(request.POST.get('animal2').lower().replace(" ", ""))
        animal3 = normalize(request.POST.get('animal3').lower().replace(" ", ""))
        respuesta = animal1+animal2+animal3
        cve = request.POST.get('txtCve')
        print("respuesta ", respuesta)
        if animal1 == "leon":
            resultado += 1
        if animal2 == "hipopotamo":
            resultado += 1
        if animal3 == "camello" or  animal3 == "dromedario":
            resultado += 1
        return makeregistermoca(cve, 4, respuesta, resultado, 3)       
    else:
        print("no entro ajax")
        return redirect("/paciente")

def moca9(request):
    if request.is_ajax():
        num = 100
        nums=[]
        resultado = 0
        cuenta = 0
        respuesta = ""
        for i in range(0,5):
            nums.append(request.POST.get('numero'+str(i+1)+'').replace(" ",""))
        cve = request.POST.get('txtCve')
        for i in range(0, 5):
            num -= 7
            if int(nums[i]) == num:
                cuenta +=1
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

def moca12(request):
    if request.is_ajax():
        resultado = 0
        cat2 = normalize(request.POST.get('categoria2').lower().replace(" ",""))
        cat3 = normalize(request.POST.get('categoria3').lower().replace(" ",""))
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
        correctas=['rostro', 'templo', 'clavel', 'rojo', 'seda']
        puntos = []
        respuesta = " "
        for i in range(0,5):
            puntos.append(int(request.POST.get('resultadop'+str(i+1)+'')))
            respuesta += normalize(request.POST.get('palabra'+str(i+1)+'').lower().replace(" ",""))
        cve = request.POST.get('txtCve')
        for i in range (0, len(correctas)):
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
        diasemana = weekday.get(normalize(request.POST.get('diasemana').lower().replace(" ","")))
        dia = normalize(request.POST.get('dia').lower().replace(" ",""))
        mes = month.get(normalize(request.POST.get('mes').lower().replace(" ","")))
        anio = normalize(request.POST.get('anio').lower().replace(" ",""))
        lugar = normalize(request.POST.get('lugar').lower().replace(" ",""))
        localidad = normalize(request.POST.get('localidad').lower().replace(" ",""))

        respuesta = str(diasemana)+'-'+dia+'-'+str(mes)+'-'+anio+'-'+lugar+'-'+localidad
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


def editP(request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    iduser = decodedToken['user_id']
    print("iduser", iduser)
    infoU = requests.get('http://127.0.0.1:8000/v1/userd/'+str(iduser)+'')
    infoP = requests.get('http://127.0.0.1:8000/v1/Pacienteuser/'+str(iduser)+'')
    if infoP.ok and infoU.ok:
        initial_dict = {
            "nvo_nombre":json.loads(infoU.content)['first_name'],
            "nvo_apellidos": json.loads(infoU.content)['last_name'],
            "nvo_nombreUsuario":json.loads(infoU.content)['username'],
            "nvo_sexo":json.loads(infoP.content)['sexo'],
            "nvo_escolaridad":json.loads(infoP.content)['escolaridad'],
            "nvo_fechaDiag":json.loads(infoP.content)['fechaDiag'] 
        }
    else:
        print("Ocurrio error en usuario ", infoU.status_code)
        print("Ocurrio error en paciente ", infoP.status_code)
    if request.method=="POST": 
        feditP = FormEditarP(request.POST, initial=initial_dict)
        #try:      
        if feditP.is_valid(): 
            payload = {
                "username": feditP.cleaned_data['nvo_nombreUsuario'],
                "first_name": feditP.cleaned_data['nvo_nombre'],
                "last_name": feditP.cleaned_data['nvo_apellidos']
            }
            updateU =  requests.put('http://127.0.0.1:8000/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
                        payload), headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
            if updateU.ok:
                print("Se pudo actualizar el usuario")
                payloadP = {
                    "sexo":feditP.cleaned_data['nvo_sexo'],
                    "escolaridad":feditP.cleaned_data['nvo_escolaridad'],
                    "fechaDiag": feditP.cleaned_data['nvo_fechaDiag']
                }
                print(payloadP)
                updateP =requests.put('http://127.0.0.1:8000/v1/editarpaciente/'+str(json.loads(infoP.content)['id']) +'', data=json.dumps(payloadP), headers={'content-type': 'application/json'})
                if updateP.ok:
                    return render(request, "Paciente/inicioPaciente.html", {"name":feditP.cleaned_data['nvo_nombre'], "access": token})
                else:
                    print(updateP.json())
            else:
                print(updateU.json())

    else:
        feditP=FormEditarP(initial=initial_dict)
    return render(request, "Paciente/editarPaciente.html", {"form": feditP, "user": iduser}) #Renderizar vista pasando el formulario como contexto