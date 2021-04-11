from django.shortcuts import render,redirect
from django.http import HttpResponse
from Cuidador.models import Pregunta, Cat_Pregunta
from .models import Paciente, Ap_Reminiscencia, Reminiscencia
import random

def inicioPa(request):
    return render(request, "Pruebas/inicioPaciente.html")

def saveAnswer(request):
    if request.method == "POST":
        cve = request.POST['cveRem']
        idR = request.POST['txtidReactivo']
        respCorrecta = Pregunta.objects.filter(idReactivo=idR)[0].respuestaCuidador
        if Cat_Pregunta.objects.filter(idReactivo=idR)[0].tipoPregunta == 'A':
            respuesta = request.POST['txtrespuestaA']
        else:
            respuesta = request.POST['respuestaOP']
            respCorrecta = respCorrecta.split("-")[int(respCorrecta[0])]
        print(respCorrecta)
        #if Pregunta.objects.get(respuestaCuidador__contains=respuesta):
        val = True
        try: 
            registro = Reminiscencia.objects.create(cveAcceso=cve, idPregunta=idR, respuestaPaciente=respuesta, valoracion= val)    
            registro.save()  
        except:
            print("No se guardo la respuesta")  

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
            return render(request, "Pruebas/reminiscencia1.html", {"preguntas":answers, "op":op, "img": img, "audio": audio})
        else:
            return redirect("/paciente/?novalid")

def rmsc2(request):
    return render(request, "Pruebas/reminiscencia2.html")

def rmsc3(request):
    return render(request, "Pruebas/reminiscencia3.html")

def moca1(request):
    return render(request, "Pruebas/tamizaje1.html")

def moca2(request):
    return render(request, "Pruebas/tamizaje2.html")

def moca3(request):
    return render(request, "Pruebas/tamizaje3.html")

def moca4(request):
    return render(request, "Pruebas/tamizaje4.html")

def editP(request):
    return render(request, "Pruebas/editarPaciente.html")