from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from Cuidador.models import Pregunta, Cat_Pregunta
from .models import Paciente, Ap_Reminiscencia, Reminiscencia
from .forms import FormEditarP
from Usuario.apiviews import PacienteUser
import random
import requests
import json

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


def moca1(request):
    return render(request, "Paciente/tamizaje1.html")

def moca2(request):
    return render(request, "Paciente/tamizaje2.html")

def moca3(request):
    return render(request, "Paciente/tamizaje3.html")

def moca4(request):
    return render(request, "Paciente/tamizaje4.html")

def editP(request, iduser):
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
                        payload), headers={'content-type': 'application/json'})
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
                    return render(request, "Paciente/inicioPaciente.html", {"name":feditP.cleaned_data['nvo_nombre'], "user_id": iduser})
                else:
                    print(updateP.json())
            else:
                print(updateU.json())

    else:
        feditP=FormEditarP(initial=initial_dict)
    return render(request, "Paciente/editarPaciente.html", {"form": feditP, "user": iduser}) #Renderizar vista pasando el formulario como contexto