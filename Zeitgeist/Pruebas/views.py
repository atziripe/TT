from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from Cuidador.models import Pregunta, Cat_Pregunta
from .models import Paciente, Ap_Reminiscencia, Reminiscencia
import random, re
from Usuarios import views
from .forms import FormEditarP
import datetime

def inicioPa(request):
     return render(request, "Usuarios/index.html")

def rmsc1(request):
    paciente = request.session.get("usuarioActual")
    if request.method=="POST":
        cve = request.POST['cveRem']
        if Ap_Reminiscencia.objects.filter(cveAcceso=cve, resultadoFinal__isnull=True):
            answers = []
            idR = []
            op= {} #{"1":[Ana, Mariana, Luisa], "84": [5,8,9]}
            img={} #{"5" : "/reminiscencia/sala.jgp", ...}
            audio = {}
            cuidador = Paciente.objects.get(nomUsuario=paciente).cuidador.nomUsuario
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
            return render(request, "Pruebas/reminiscencia1.html", {"cve": cve,"preguntas":answers, "op":op, "img": img, "audio": audio})
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
    return render(request, "Pruebas/tamizaje1.html")

def moca2(request):
    return render(request, "Pruebas/tamizaje2.html")

def moca3(request):
    return render(request, "Pruebas/tamizaje3.html")

def moca4(request):
    return render(request, "Pruebas/tamizaje4.html")

#def contexto(request, feditP):
#    usuarioActual = request.session.get("usuarioActual")
#    user = Paciente.objects.get(nomUsuario = usuarioActual)
#    feditP.nvo_nombre = user.nombre
#    feditP.nvo_nombreUsuario = user.nomUsuario
#    feditP.nvo_correo = user.correo
#    feditP.nvo_contrasena = user.contrasena
#    feditP.nvo_sexo = user.sexo
#    feditP.nvo_fechaNac = user.fechaNac
#    feditP.nvo_escolaridad = user.escolaridad
#    feditP.nvo_fechaDiag = user.fechaDiag 


def editP(request):    
    base = "Pruebas/basePacientes.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
    pacienteActual = Paciente.objects.get(nomUsuario=request.session.get("usuarioActual"))
    if request.method=="POST": 
        feditP = FormEditarP(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if feditP.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',request.POST['nvo_correo'].lower()): #Validación de formulario y correo electrónico
                pwd = request.POST['nvo_contrasena']
                curr_pwd = request.POST['confirmacion_cont']
                nomUser = request.POST['nvo_nombreUsuario']
                fecha = datetime.date.today()
                fechaHoy = str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
                fechaDiag = feditP.cleaned_data['nvo_fechaDiag']
                fechaNac = feditP.cleaned_data['nvo_fechaNac']

                if fechaNac < fecha and fechaNac < fechaDiag and fechaDiag < fecha:
                    if str(fechaDiag.year) < '1890' or str(fechaNac.year) < '1890':
                            #raise ValidationError("La fecha de diagnostico y fecha de nacimiento no pueden registrarse en el día que usted indica, por favor compruebe las fechas y vuelva a escribirlas. Asegúrese de escribir un año mayor a 1890 y que las fechas no sobrepasen a la fecha actual.")
                            #print ("Fechas no Validas")
                        return redirect("/paciente/editarP/?fechas_no_validas")
                            # La fecha de diagnostico y fecha de nacimiento no pueden registrarse en el día que usted indica, por favor compruebe las fechas y vuelva a escribirlas. Asegúrese de escribir un año mayor a 1890 y que las fechas no sobrepasen a la fecha actual.
                else:
                    return redirect("/paciente/editarP/?fechas_no_validas")

                if nomUser != pacienteActual.nomUsuario: #Si el nombre de usuario no se modifico, nos saltamos validación de existencia.
                    if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                        return redirect("/paciente/editarP/?ya_existe_registro")
                
                pass_valida = views.ValidarContrasena(pwd) #Validacion de contraseña:
                if pass_valida == False:
                    return redirect("/paciente/editarP/?contrasena_invalida")
            else:
                return redirect("/paciente/editarP/?no_valido")        
	        #Checar que contraseña actual es correcta
            if curr_pwd == pacienteActual.contrasena:
	            #Si coincide, se aplica el cambio solicitado

                pacienteActual.nomUsuario = nomUser
                pacienteActual.nombre=request.POST['nvo_nombre']
                pacienteActual.contrasena= pwd
                pacienteActual.correo=request.POST['nvo_correo']
                pacienteActual.sexo=request.POST['nvo_sexo']
                pacienteActual.fechaNac = fechaNac
                pacienteActual.fechaDiag = fechaDiag
                pacienteActual.escolaridad = request.POST['nvo_escolaridad']
                pacienteActual.save()

                return redirect("/login/?edicion_valida")
            else:
                return redirect("/paciente/editarP/?error_contrasena")
        except:
            return redirect("/paciente/editarP/?no_valido")
    else:
        feditP=FormEditarP()
        #contexto(request, feditP) #Se reciben los datos previos por default
    return render(request, "Pruebas/editarPaciente.html", {"form": feditP, "base": base}) #Renderizar vista pasando el formulario como contexto