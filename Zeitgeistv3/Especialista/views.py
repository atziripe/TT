from django.shortcuts import render,  redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Sum
from Usuario import views
import os
from .forms import FormEditarE, FormMensaje
from .models import Mensaje
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User
from Paciente.models import Ap_Screening, Screening, Ap_Reminiscencia, Ent_Cogn
from Usuario.models import Paciente, Especialista, User
import random, re, json, jwt, requests
import string, datetime
import numpy as np
#Para el reporte
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import date, datetime

def inicioEsp(request, token):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': "Especialista"})
    except:
        print("No se accedió a la página con credenciales de usuario válidas")
        return render(request, "Usuarios/index.html", {"session_expired": True})


def editE(request, token, tipo, name):
    try:  
        base = "Especialista/baseEspecialista.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        print("iduser", iduser)
        infoU = requests.get('http://127.0.0.1:8000/v1/userd/'+str(iduser)+'')
        infoE = requests.get('http://127.0.0.1:8000/v1/Especialistauser/'+str(iduser)+'')

        if infoE.ok and infoU.ok:
            initial_dict = {
                "nvo_nombre":json.loads(infoU.content)['first_name'],
                "nvo_apellidos": json.loads(infoU.content)['last_name'],
                "nvo_correo":json.loads(infoU.content)['email'],
                "nvos_datos_generales":json.loads(infoE.content)['datos_generales'],
                "nvo_numPacientes":json.loads(infoE.content)['numPacientes'], 
            }
        else:
            print("Ocurrio error en usuario", infoU.status_code)
            print("Ocurrio error en especialista", infoE.status_code)
        if request.method=="POST": 
            feditE = FormEditarE(request.POST, initial=initial_dict)
            #try:      
            if feditE.is_valid(): 
                payload = {
                    "first_name": feditE.cleaned_data['nvo_nombre'],
                    "last_name": feditE.cleaned_data['nvo_apellidos'],
                    "username": json.loads(infoU.content)['username'],
                    "email": feditE.cleaned_data['nvo_correo']
                }
                updateU =  requests.put('http://127.0.0.1:8000/v1/editarperfil/'+str(iduser)+'', data=json.dumps(
                            payload), headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
                if updateU.ok:
                    print("Se pudo actualizar el usuario")
                    payloadE = {
                        "datos_generales":feditE.cleaned_data['nvos_datos_generales'],
                        "numPacientes":feditE.cleaned_data['nvo_numPacientes'],
                    }
                    print(payloadE)
                    updateE =requests.put('http://127.0.0.1:8000/v1/editarespecialista/'+str(json.loads(infoE.content)['id']) +'', data=json.dumps(payloadE), headers={'content-type': 'application/json'})
                    if updateE.ok:
                        return render(request, "Especialista/inicioEspecialista.html", {"name":feditE.cleaned_data['nvo_nombre'], "tipo": tipo, "access": token, "modified" : True})
                    else:
                        print(updateE.json())
                else:
                    print(updateU.json())
                    print("No se pudo hacer el registro del usuario")
                    return render(request, "Especialista/editarEspecialista.html", {"name":feditE.cleaned_data['nvo_nombre'],"form": feditE, "user": iduser, "access": token, "tipo": tipo, "already_exists": True, "base": base})

        else:
            feditE=FormEditarE(initial=initial_dict)
        return render(request, "Especialista/editarEspecialista.html", {"name": name, "form": feditE, "user": iduser, "base": base, "tipo": tipo, "access": token}) #Renderizar vista pasando el formulario como contexto
    except:
        print("Las credenciales de usuario han expirado o existe algún problema con el ingreso")
        return render(request, "Usuarios/index.html")


def cveAcceso(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    try: 
        if request.method=="POST":
            userp = User.objects.filter(username=request.POST['nomUsu'])[0].id
            print("userp ", userp)
            pacient = Paciente.objects.filter(user_id=userp)[0]
            print("pacient ", pacient)
            decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = decodedToken['user_id']
            fecha = datetime.now()
            fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
            clave = str(fecha.day)+str(fecha.month)+str(fecha.year)[2:4]+str(fecha.hour)+str(fecha.minute)+str(user)+random.choice(string.ascii_uppercase)+str(random.randint(0,9))+random.choice(string.ascii_uppercase)
            print(clave)
            if Ap_Screening.objects.filter(resultadoFinal__isnull=True ,paciente=pacient): 
                print("No se pudo crear la sesión de tamizaje")
                return render(request, "Especialista/inicioEspecialista.html",{"exito": 'false', 'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})
            else:
                screening = Ap_Screening.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy)
                screening.save()
                print(clave)
                return render(request, "Especialista/inicioEspecialista.html",{'clave':clave, 'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})
    except:
        print("El paciente indicado no es atendido por este especialista")
        return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': tipo, 'error_paciente': True})
    return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})


def obtenerInfoUsers(usersIDList_req, idEspecialista): #Obtenemos la informacion de los pacientes del especialista, incluyendo notificación si no tienen cuidador 
    lista_infoP = {}
    usersID = json.loads(usersIDList_req.content)
    escolaridad_values ={ 'N':'Ninguna', 'PR':'Primaria', 'SC':'Secundaria', 'BCH':'Bachillerato', 'SUP':'Licenciatura o superior'}
    sexo_values = {'F': "Femenino", 'M': "Masculino"}

    for user in usersID:
        cuidador_uname = -1 #Inicializamos a -1 estas dos variables que seran para el paciente sin relaciones con otros usuarios
        id_paciente = user['id'] #Id de usuario de paciente
        infoP_req = requests.get('http://127.0.0.1:8000/v1/pacientsd/'+str(id_paciente)+'')
        try:
            doctor_dePa = json.loads(infoP_req.content)['especialista']

            if int(doctor_dePa) == int(idEspecialista):
                infoP = json.loads(infoP_req.content)  #Sacamos datos del paciente si fue asignado al especialista
                id_user_Pa = infoP['user']
                infoUserP_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user_Pa)+'')
                infoUserP = json.loads(infoUserP_req.content)
                
                lista_infoP[infoUserP['username']] = infoUserP
                lista_infoP[infoUserP['username']]['idPaciente'] = infoP['id']
                lista_infoP[infoUserP['username']]['sexo'] = sexo_values[infoP['sexo']]
                fechaNac_date = datetime.strptime(infoP['fechaNac'], '%Y-%m-%d') 
                lista_infoP[infoUserP['username']]['fechaNac'] = fechaNac_date.strftime('%d / %m / %Y')
                lista_infoP[infoUserP['username']]['escolaridad'] = escolaridad_values[infoP['escolaridad']]
                fechaDiag_date = datetime.strptime(infoP['fechaDiag'], '%Y-%m-%d') 
                lista_infoP[infoUserP['username']]['fechaDiag'] = fechaDiag_date.strftime('%d / %m / %Y')

                id_cuidador = json.loads(infoP_req.content)['cuidador'] #Obtenemos nombre completo del Cuidador de cada paciente
                id_user_c = Cuidador.objects.get(id=id_cuidador).user_id
                infoCui_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user_c)+'')
                cuidador_name = json.loads(infoCui_req.content)['first_name'] + ' ' + json.loads(infoCui_req.content)['last_name']
                    
                lista_infoP[infoUserP['username']]["cuidador_name"] = cuidador_name
        except:
            print("Hay un paciente que no tiene asignado doctor aún")

    return lista_infoP 
    

def verPacientes(request, token, tipo):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser = decodedToken['user_id']
        idEspecialista = Especialista.objects.get(user_id=iduser).id #Obtenemos ID de user

        if not Paciente.objects.filter(especialista=idEspecialista).exists(): #Si no tenemos pacientes, no se genera tabla 
            return render(request, "Especialista/visualizarPacientes.html", {'No_tiene_pacientes': True, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, "base": "Especialista/baseEspecialista.html"})
        else:
            pacientesIDlist_req = requests.get('http://127.0.0.1:8000/v1/listpacient/', headers={'content-type': 'application/json', "Authorization": "Bearer "+ token +""})
            listaPacientes = obtenerInfoUsers(pacientesIDlist_req, idEspecialista)
            return render(request, "Especialista/visualizarPacientes.html", {"listPatients": listaPacientes, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, "base": "Especialista/baseEspecialista.html"})
    except:
        print("Error de autenticación")
        return render(request, "Usuarios/index.html", {"session_expired": True})



def mensajeCuidador(request, token, tipo, pacienteC):
    try:
        decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
        iduser_Esp = decodedToken['user_id']
        esp_inst = Especialista.objects.get(user_id=iduser_Esp)
        fecha = datetime.datetime.now()
        fechahoy= str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)

        infoPaciente = requests.get('http://127.0.0.1:8000/v1/pacientsd/'+str(pacienteC)+'')
        id_cuidador = json.loads(infoPaciente.content)['cuidador'] #Obtenemos nombre de usuario y nombre completo del Cuidador 
        cui_inst= Cuidador.objects.get(id=id_cuidador)
        id_user_c = cui_inst.user_id
        infoCui_req = requests.get('http://127.0.0.1:8000/v1/userd/'+str(id_user_c)+'')
        cuidador_name = json.loads(infoCui_req.content)['first_name'] + ' ' + json.loads(infoCui_req.content)['last_name']       
        initial_dict = { "cuidador": cuidador_name}

        if request.method=="POST": 
            fmsg = FormMensaje(request.POST, initial=initial_dict)
                
            if fmsg.is_valid(): 
                mensaje = Mensaje.objects.create(especialista=esp_inst, cuidador=cui_inst,  mensaje= fmsg.cleaned_data['mensaje'],fechaEnvio=fechahoy)
                mensaje.save()
                return render(request, "Especialista/mensajesCuidador.html", {'form': fmsg, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, 'success_sentM': True, 'base': "Especialista/baseEspecialista.html"})
            else:
                return render(request, "Especialista/mensajesCuidador.html", {'form': fmsg, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, 'error_sentM': True, 'base': "Especialista/baseEspecialista.html"})
            
        else:
            fmsg=FormMensaje(initial=initial_dict)
            return render(request, "Especialista/mensajesCuidador.html", {'form': fmsg, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo, 'initial': True, 'base': "Especialista/baseEspecialista.html"})
    
    except:
        print("Error en la vista de mensajes del cuidador")
        return render(request, "Usuarios/index.html", {"session_expired": True})

def califmoca(request, cve, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    r14 = Screening.objects.filter(idApp= str(cve)+"14")[0].respuestaT.split("-")
    lugar = r14[4]
    localidad = r14[5]
    imagen = Screening.objects.filter(idApp= str(cve)+"3")[0].respuestaImg
    return render(request, "Especialista/calificarmoca.html", {"cve":cve, "lugar":lugar, "localidad":localidad, "imagen":imagen, 'name': decodedToken['first_name'], 'access': token, 'tipo': tipo})



def modalfinishMoca(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    if request.method=="POST":
        cve = request.POST.get('cvesave')
        if request.POST.get('contorno') == None:
            contorno = 0
        else:
            contorno = int(request.POST.get('contorno'))

        if request.POST.get('numeros') == None:   
            numeros = 0
        else:
            numeros = int(request.POST.get('numeros'))
        if request.POST.get('agujas') == None:
            agujas = 0
        else:
            agujas = int(request.POST.get('agujas'))
        if request.POST.get('lugar') == None:
            lugar = 0
        else:
            lugar = int(request.POST.get('lugar'))
        if request.POST.get('localidad') == None:
            localidad  = 0
        else:
            localidad = int(request.POST.get('localidad'))
        
        Screening.objects.filter(idApp=cve+"3").update(puntajeReactivo=contorno+numeros+agujas, respuestaT=str(contorno)+"-"+str(numeros)+"-"+str(agujas))

        pactuallugar = Screening.objects.filter(idApp=cve+"14")[0].puntajeReactivo
        reactivolugar = Screening.objects.filter(idApp=cve+"14").update(puntajeReactivo=pactuallugar+lugar+localidad)

        respuestaactualLugar = Screening.objects.filter(idApp=cve+"14")[0].respuestaT
        cambio = respuestaactualLugar.split("-")[4]

        nuevoresplugar = Screening.objects.filter(idApp=cve+"14").update(respuestaT = respuestaactualLugar[0:respuestaactualLugar.find(cambio)]+str(lugar)+"-"+str(localidad))
        suma = Screening.objects.filter(cveAcceso=cve).aggregate(Sum('puntajeReactivo'))["puntajeReactivo__sum"]
        #Obtener escolaridad del paciente para subir punto si es >= 12 años
        id_paciente = Ap_Screening.objects.filter(cveAcceso=cve)[0].paciente.id
        escolaridad = Paciente.objects.filter(id=id_paciente)[0].escolaridad
        if escolaridad == "BCH" or escolaridad =="SUP":
            suma += 1
        editApSc = Ap_Screening.objects.filter(cveAcceso=cve).update(resultadoFinal=suma)
        return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})
    else:
        print("no entro ajax")


def reportes(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    especialista = Especialista.objects.filter(user_id=user)[0].id
    pacientes = []
    longitud = len(Paciente.objects.filter(especialista=especialista))
    for i in range(0,longitud):        
        pacientes.append(Paciente.objects.filter(especialista=especialista)[i].id)
    claves = []
    for i in pacientes:        
        clave = Ap_Screening.objects.filter(paciente=i)
        if clave:
            x = 1
            userP = Paciente.objects.filter(id=clave[0].paciente_id)[0].user_id
            nameP = User.objects.filter(id=userP)[0].first_name + " " + User.objects.filter(id=userP)[0].last_name
            for c in clave:
                if (Screening.objects.filter(idApp=c.cveAcceso+"13")):
                    recuerdoD = int(Screening.objects.filter(idApp=c.cveAcceso+"13")[0].puntajeReactivo)
                    suma = int(recuerdoD/3)
                    puntajeF = int(c.resultadoFinal-15+suma)
                else:
                    puntajeF = 0

                claves.append({'index':x,'datos':c,'nombre':nameP, 'puntaje':puntajeF})
                x+=1
    return render(request, "Especialista/reportes.html", {'claves': claves, 'access': token, 'tipo': tipo, 'name': decodedToken['first_name']})

def encuentra(cadena, frase):
    if frase.find(cadena) == -1:
        return False
    else:
        return True

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def moca(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = decodedToken['user_id']
    if request.method=="POST":
        especialista = Especialista.objects.filter(user_id=user)[0].id
        aplicador = User.objects.filter(id=user)[0].first_name + " " + User.objects.filter(id=user)[0].last_name
        clave = request.POST.get('claveA')
        #pathF = str(os.path.dirname(os.path.abspath(clave+".pdf"))).replace('\\','/') + "/" + clave+".pdf"
        #print(pathF)
        tamizaje = Screening.objects.filter(cveAcceso=clave)
        puntajes=[]
        cadenaCal = ""
        imgs = []
        for i in tamizaje:
            puntaje = {'nReac':i.idReactivo, 'pts':i.puntajeReactivo}
            puntajes.append(puntaje)
            if i.idReactivo == 2:
                imagen = {'nReac':i.idReactivo, 'img': i.respuestaImg }
                imgs.append(imagen)
                cadenaCal = str(i.respuestaT)
                print(cadenaCal)
            elif i.idReactivo == 3:
                imagen = {'nReac':i.idReactivo, 'img': i.respuestaImg }
                imgs.append(imagen)
        aplicacion = Ap_Screening.objects.filter(cveAcceso=clave)
        resultado = int(aplicacion[0].resultadoFinal) - 15 
        #print(aplicacion[0].paciente_id)
        usuarioP = Paciente.objects.filter(id=aplicacion[0].paciente_id)[0].user_id
        nombreP = User.objects.filter(id=usuarioP)[0].first_name + " " + User.objects.filter(id=usuarioP)[0].last_name
        datos = {'fecha':str(aplicacion[0].fechaAp), 'nombre': nombreP}
        #print(datos)
        paciente = Paciente.objects.filter(id=aplicacion[0].paciente_id)
        nac = str(paciente[0].fechaNac)
        if paciente[0].sexo == 'F':
            gender = "Femenino"
        else:
            gender = "Masculino"
        if paciente[0].sexo == 'M':
            estudios = 'Ninguna'
        elif paciente[0].escolaridad == 'PR':
            estudios = 'Primaria'
        elif paciente[0].escolaridad == 'SC':
            estudios = 'Secundaria'
        elif paciente[0].escolaridad == 'BH':
            estudios = 'Bachillerato'
        else:
            estudios = 'Licenciatura o superior'
        fecha = str(aplicacion[0].fechaAp)
        #print(fecha)
        w, h = letter
        fechaP = Paciente.objects.filter(id=aplicacion[0].paciente_id)[0].fechaNac
        #print(fechaP)
        primerL = "Nombre: " + str(nombreP)
        segundaL = "Fecha de nac.: " + str(fechaP) + "       Sexo:" + str(gender)
        terceraL = "Escolaridad: " + str(estudios) + "       FECHA: " + str(fecha)
        c = canvas.Canvas(clave+".pdf", pagesize = letter)
        location = str(os.path.dirname(os.path.abspath("fondo-reporte.jpg"))).replace('\\','/')
        c.drawImage(location+'/staticfiles/images/fondo-reporte.jpg', 0, 0, width=600, height=800) # Fondo
        c.setFont("Helvetica", 9)
        c.drawString(315, h - 60, primerL) # Nombre
        c.drawString(315, h - 70, segundaL) # Fecha nacimiento y sexo
        c.drawString(315, h - 80, terceraL) # Escolaridad y fecha aplicación
        for i in imgs:
            if i['nReac'] == 2:
                c.drawImage(location+"/media/"+str(i['img']), 250, h - 260, width=80, height=90) #cubo
            else:
                c.drawImage(location+"/media/"+str(i['img']), 400, h - 240, width=90, height=120) #reloj
        c.setFont("Helvetica", 10)
        
        for p in puntajes:
            #print(p)
            if p['nReac'] == 1:
                c.drawString(184, h - 275, str(p['pts'])) # Cadena
                ve1 = p['pts']
            elif p['nReac'] == 2:
                c.drawString(341, h - 275, str(p['pts'])) # Cubo
                ve2 = p['pts']
            elif p['nReac'] == 3:
                ve3 = p['pts']
            elif p['nReac'] == 4:                
                c.drawString(550, h - 411, str(p['pts'])) # Final Identificación
            elif p['nReac'] == 6:
                c.drawString(455, h - 466, str(p['pts'])) # Números orden
                atn1 = str(p['pts'])
            elif p['nReac'] == 7:
                c.drawString(455, h - 478, str(p['pts'])) # Números invertidos
                atn2 = str(p['pts'])
            elif p['nReac'] == 8:
                c.drawString(285, h - 505, str(p['pts'])) # Atención (Golpes)
                c.drawString(550, h - 505, str(p['pts'])) # Final Atención 2
            elif p['nReac'] == 9:
                c.drawString(550, h - 529, str(p['pts'])) # Final Atención 3
            elif p['nReac'] == 10:
                c.drawString(550, h - 555, str(p['pts'])) # Final Lenguaje 1
            elif p['nReac'] == 11:
                c.drawString(427, h - 572, str(p['pts'])) # Palabras 1 min
                c.drawString(550, h - 571, str(p['pts'])) # Final Lenguaje 2
            elif p['nReac'] == 12:
                c.drawString(550, h - 589, str(p['pts'])) # Final Abstración
            elif p['nReac'] == 13:
                c.drawString(482, h - 649, str(p['pts'])) # MIS Puntos Tabla
                c.drawString(415, h - 683, str(p['pts'])) # MIS Puntos
                puntos = int(p['pts']/3)
                resultado = resultado + puntos
                c.drawString(550, h - 605, str(puntos)) # Final Recuerdo Diferido
            elif p['nReac'] == 14:
                c.drawString(550, h - 666, str(p['pts'])) # Final Orientación
      
        for i in tamizaje:
            if i.idReactivo == 4: # Animales
                respuestaAn = i.respuestaT
            if i.idReactivo == 3: # Reloj
                respuestaRe = i.respuestaT 
            if i.idReactivo == 5: # Palabras
                respuestaTabla = i.respuestaT
            if i.idReactivo == 9: # Restas
                respuestaSu = i.respuestaT
            if i.idReactivo == 10: # Frases
                respuestaFr = i.respuestaT 
            if i.idReactivo == 11: # Palabras F
                respuestaPa = i.respuestaT
            if i.idReactivo == 12: # Abstraccion
                respuestaTr = i.respuestaT
            if i.idReactivo == 14: # Orientación
                respuestaOr = i.respuestaT
        
        # Para calificacion de reloj
        respuestaRe = respuestaRe.split('-')
        c.drawString(390, h - 275, respuestaRe[0]) # Reloj 1
        c.drawString(448, h - 275, respuestaRe[1]) # Reloj 2
        c.drawString(510, h - 275, respuestaRe[2]) # Reloj 3
        # Para Identificacion
        if respuestaAn.find('leon') == -1:
            c.drawString(185, h - 411, "0") # León
        else:
            c.drawString(185, h - 411, "1") # León
        if respuestaAn.find('rinoceronte') == -1:
            c.drawString(343, h - 411, "0") # Rinoceronte
        else:
            c.drawString(343, h - 411, "1") # Rinoceronte
        if respuestaAn.find('camello') == -1:
            if respuestaAn.find('dromedario') == -1:
                c.drawString(499, h - 411, "0") # Camello
            else:
                c.drawString(499, h - 411, "1") # Camello
        else:
            c.drawString(499, h - 411, "1") # Camello
        # Atención - palabras
        respuestaPa = respuestaPa.split(',')
        c.drawString(445, h - 572, str(len(respuestaPa))) # Num. total
        # Lenguaje
        respuestaFr = respuestaFr.split('-')
        print(respuestaFr[0])
        print(respuestaFr[1])
        if encuentra("solosequeletocajuanayudarhoy", respuestaFr[0]):
            c.drawString(278, h - 548, "1") # Frase 1 Correcta
        else: 
            c.drawString(278, h - 548, "0") # Frase 1 Equivocada
        if encuentra("elgatosiempreseescondedebajodelsofacuandohayperrosenlahabitacion", respuestaFr[0]):
            c.drawString(422, h - 556, "1") # Frase 2
        else:
            c.drawString(422, h - 556, "0") # Frase 2 incorrecta
        # Respuestas tabla
        respuestaTabla = respuestaTabla.split('-')
        if encuentra('rostro', respuestaTabla[0]):
            c.drawString(315, h - 444, "*") # Rostro 1er
        if encuentra('seda', respuestaTabla[0]):
            c.drawString(365, h - 444, "*") # Seda 1er
        if encuentra('templo', respuestaTabla[0]):
            c.drawString(415, h - 444, "*") # Templo 1er
        if encuentra('clavel', respuestaTabla[0]):
            c.drawString(463, h - 444, "*") # Clavel 1er
        if encuentra('rojo', respuestaTabla[0]):
            c.drawString(515, h - 444, "*") # Rojo 1er
        if encuentra('rostro', respuestaTabla[1]):
            c.drawString(315, h - 456, "*") # Rostro 2da
        if encuentra('seda', respuestaTabla[1]):
            c.drawString(365, h - 456, "*") # Seda 2da
        if encuentra('templo', respuestaTabla[1]):
            c.drawString(415, h - 456, "*") # Templo 2da
        if encuentra('clavel', respuestaTabla[1]):
            c.drawString(463, h - 456, "*") # Clavel 2da
        if encuentra('rojo', respuestaTabla[1]):
            c.drawString(515, h - 456, "*") # Rojo 2da
            
        # Abstraccion
        if encuentra("transporte", respuestaTr):
            c.drawString(305, h - 590, "1") # Tren-bicicleta
        else:
            c.drawString(305, h - 590, "0") # Tren-bicicleta
        if encuentra("medi", respuestaTr) or encuentra("herramienta", respuestaTr):
            c.drawString(392, h - 590, "1") # Reloj-regla
        else:
            c.drawString(392, h - 590, "0") # Reloj-regla
        
        # Orientacion
        respuestaOr = respuestaOr.split('-')
        c.drawString(312, h - 666, respuestaOr[0]) # Día de la semana
        c.drawString(122, h - 666, respuestaOr[1]) # día
        c.drawString(187, h - 666, respuestaOr[2]) # Mes
        c.drawString(250, h - 666, respuestaOr[3]) # Año 
        c.drawString(424, h - 666, respuestaOr[4]) # Lugar
        c.drawString(485, h - 666, respuestaOr[5]) # Localidad

        # Restas
        print(encuentra("93", respuestaSu))
        if encuentra("93", respuestaSu):
            print("Entre")
            c.drawString(187, h - 520, "1") # Resta 1
        if encuentra("86", respuestaSu):
            c.drawString(257, h - 520, "1") # Resta 2
        if encuentra("79", respuestaSu):
            c.drawString(324, h - 520, "1") # Resta 3
        if encuentra("72", respuestaSu):
            c.drawString(402, h - 520, "1") # Resta 4
        if encuentra("65", respuestaSu):
            c.drawString(464, h - 520, "1") # Resta 5

        visoesp = ve1 + ve2 + ve3
        c.drawString(550, h - 275, str(visoesp)) # Final Visuoespacial
        atencion = int(atn1) + int(atn2)
        c.drawString(550, h - 478, str(atencion)) # Final Atención 1
        c.drawString(115, h - 695, aplicador) # Aplicador
        c.drawString(535, h - 702, str(resultado)) # Final Total
        c.showPage()
        c.save()
        
        with open(location+"/"+clave+'.pdf', 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=MoCA'+clave+'.pdf'
            return response   
        pdf.closed
    
    return render(request, "Especialista/moca-pdf.html",{'datos':datos, 'imagenes':imgs, 'name': decodedToken['first_name'], 'access':token, 'tipo': tipo})

def datosG(clave, aplicaciones):
    tam  = []
    vee = ide = mem = atn = leng = abst = recd = ort = 0
    datos = []
    for tamizaje in aplicaciones:
        if tamizaje.idReactivo <= 3:
            vee += tamizaje.puntajeReactivo
        elif tamizaje.idReactivo == 4: # identificación
            ide = tamizaje.puntajeReactivo
        elif tamizaje.idReactivo == 5: # memoria
            mem = tamizaje.puntajeReactivo
        elif 6 <= tamizaje.idReactivo <= 9 : # atención
            atn += tamizaje.puntajeReactivo
        elif 10 <= tamizaje.idReactivo <= 11: # lenguaje
            leng += tamizaje.puntajeReactivo
        elif tamizaje.idReactivo == 12: # abstración
            abst = tamizaje.puntajeReactivo
        elif tamizaje.idReactivo == 13: #recuerdo diferido
            recd = int(tamizaje.puntajeReactivo/3)
        elif tamizaje.idReactivo == 14 : #orientación
            ort = tamizaje.puntajeReactivo
        else:
            print("Ya terminé")
        
    datos.append(vee)
    datos.append(ide)
    #datos.append(mem)
    datos.append(atn)
    datos.append(leng)
    datos.append(abst)
    datos.append(recd)
    datos.append(ort)
    #print(datos)
    return datos


def get_max(a, b):
    if a > b:
        return a
    else:
        return b

def graphic(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    if request.method=="POST":
        clave = request.POST.get('clave')
        index = int(request.POST.get('index'))
        print(clave)
        print(index)
        paciente = Ap_Screening.objects.filter(cveAcceso=clave)[0].paciente_id
        userP = Paciente.objects.filter(id=paciente)[0].user_id
        nombreP = User.objects.filter(id=userP)[0].first_name + " " + User.objects.filter(id=userP)[0].last_name
        tamizajes = Ap_Screening.objects.filter(paciente=paciente)
        j = 1
        fechas = []
        sesiones = []
        for t in tamizajes:
            fechas.append(str(t.fechaAp))
            tamizaje = {'clave': t.cveAcceso, 'fecha': t.fechaAp, 'resultado': t.resultadoFinal}
            sesiones.append(tamizaje)
        datos = {'nombre': nombreP, 'fecha1': fechas[index-1], 'fecha2':fechas[index-2]}
        tam = []
        i = len(tamizajes)
        #print(sesiones)
        index = index -1 # indice del array
        if index == 1:
            for i in range(0, index+1):
                #print(sesiones[i]['clave'])
                aplicaciones = Screening.objects.filter(cveAcceso=sesiones[i]['clave'])
                prueba = datosG(sesiones[i]['clave'], aplicaciones)
                tam.append(prueba)
        else:
            for i in range(index-1, index+1):
                #print(sesiones[i]['clave'])
                aplicaciones = Screening.objects.filter(cveAcceso=sesiones[i]['clave'])
                prueba = datosG(sesiones[i]['clave'], aplicaciones)
                tam.append(prueba)
        
        categorias = ['Visuoespacial/ejecutiva', 'Identificación', 'Atención', 'Lenguaje', 'Abstracción', 'Recuerdo Diferido', 'Orientación']
        tabla = []
        for i in range(0,7):
            diferencia = tam[0][i] - tam[1][i]
            row = {'name': categorias[i], 'm1': tam[0][i], 'm2': tam[1][i], 'dif': diferencia}
            tabla.append(row)

        dataTam = []
        for i in range(0,2):
            dataTam.append({'session': i, 'data': tam[i]} )

        ##Predicado 1
        today = date.today().year
        fechaNac = Paciente.objects.filter(id=paciente)[0].fechaNac.year
        edad = float(today - fechaNac)
        predicado1 = round(((0.01579*edad)-0.50526)*100, 1)

        ##Predicado 2
        #Primera función --> frecuencia de tratamiento no farmacológico
        hoy = date.today() 
        mespasado = datetime(hoy.year, hoy.month-1, hoy.day)
        rem = Ap_Reminiscencia.objects.filter(paciente_id=paciente, fechaAp__range=[mespasado, hoy]).count()
        ec = Ent_Cogn.objects.filter(paciente_id=paciente, fechaAp__range=[mespasado, hoy]).count()
        frecuencia = ((rem + ec)-1)/7
        
        #Segunda función --> Diferencia de puntajes entre el primer y último moca
        primermoca = Ap_Screening.objects.filter(paciente_id=paciente).order_by('fechaAp')[0].resultadoFinal
        ultimomoca = Ap_Screening.objects.filter(paciente_id=paciente).latest('fechaAp').resultadoFinal
        dif = float(ultimomoca - primermoca)
        diferencia = -0.0625*dif+0.7

        predicado2  = round(get_max(frecuencia, diferencia) * 100, 1)
    return render(request, "Especialista/graficas.html",{'predicado1': predicado1, 'predicado2':predicado2, 'datos':datos,'mocas':dataTam, 'tabla': tabla, 'name': decodedToken['first_name'], 'access':token, 'tipo': "Especialista"})
