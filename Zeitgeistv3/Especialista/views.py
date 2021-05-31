from django.shortcuts import render,  redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db.models import Sum
from Usuario import views
from .forms import FormEditarE, FormMensaje
from .models import Mensaje
from Usuario.models import Paciente, Cuidador, Especialista, Administrador
from django.contrib.auth.models import User
from Paciente.models import Ap_Screening, Screening
from Usuario.models import Paciente, Especialista, User
import random, re, json, jwt, requests
import string, datetime
# Para reporte
#import docx
#from docx.enum.text import WD_ALIGN_PARAGRAPH
#from docx.shared import Inches, Pt
#from docx2pdf import convert
#import pythoncom 
#import pypandoc
#from pypandoc.pandoc_download import download_pandoc
#import sys, os
#import comtypes.client

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
            fecha = datetime.datetime.now()
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
                fechaNac_date = datetime.datetime.strptime(infoP['fechaNac'], '%Y-%m-%d') 
                lista_infoP[infoUserP['username']]['fechaNac'] = fechaNac_date.strftime('%d / %m / %Y')
                lista_infoP[infoUserP['username']]['escolaridad'] = escolaridad_values[infoP['escolaridad']]
                fechaDiag_date = datetime.datetime.strptime(infoP['fechaDiag'], '%Y-%m-%d') 
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

def califmoca(request, cve):
    r14 = Screening.objects.filter(idApp= str(cve)+"14")[0].respuestaT.split("-")
    lugar = r14[4]
    localidad = r14[5]
    imagen = Screening.objects.filter(idApp= str(cve)+"3")[0].respuestaImg
    return render(request, "Especialista/calificarmoca.html", {"cve":cve, "lugar":lugar, "localidad":localidad, "imagen":imagen})



def modalfinishMoca(request, token, tipo):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
    if request.method=="POST":
        cve = request.POST.get('cvesave')
        contorno = int(request.POST.get('contorno'))
        numeros = int(request.POST.get('numeros'))
        agujas = int(request.POST.get('agujas'))
        lugar = int(request.POST.get('lugar'))
        localidad = int(request.POST.get('localidad'))
        reactivoreloj = Screening.objects.filter(idApp=cve+"3").update(puntajeReactivo=contorno+numeros+agujas, respuestaT=str(contorno)+"-"+str(numeros)+"-"+str(agujas))
        pactuallugar = Screening.objects.filter(idApp=cve+"14")[0].puntajeReactivo
        reactivolugar = Screening.objects.filter(idApp=cve+"14").update(puntajeReactivo=pactuallugar+lugar+localidad)
        suma = Screening.objects.filter(cveAcceso=cve).aggregate(Sum('puntajeReactivo'))["puntajeReactivo__sum"]
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
    numero = len(Ap_Screening.objects.filter(paciente='1'))
    claves = []
    for i in pacientes:        
        clave = Ap_Screening.objects.filter(paciente=i)
        i = len(Ap_Screening.objects.filter(paciente=i))
        userP = Paciente.objects.filter(id=clave[0].paciente_id)[0].user_id
        nameP = User.objects.filter(id=userP)[0].first_name + " " + User.objects.filter(id=userP)[0].last_name
        for c in clave:
            claves.append({'index':i,'datos':c,'nombre':nameP})
            i=i-1
    pruebas = []
    return render(request, "Especialista/reportes.html", {'claves': claves, 'access': token, 'tipo': tipo, 'name': decodedToken['first_name']})

def moca(request):
    if request.method=="POST":
        clave = request.POST.get('claveA')
        tamizaje = Screening.objects.filter(cveAcceso=clave)
        puntajes=[]
        imgs = []
        for i in tamizaje:
            puntaje = {'nReac':i.idReactivo, 'pts':i.puntajeReactivo}
            puntajes.append(puntaje)
            if i.idReactivo == 2:
                imagen = {'nReac':i.idReactivo, 'img': i.respuestaImg }
                imgs.append(imagen)
            elif i.idReactivo == 3:
                imagen = {'nReac':i.idReactivo, 'img': i.respuestaImg }
                imgs.append(imagen)
        
        print(puntajes)
        aplicacion = Ap_Screening.objects.filter(cveAcceso=clave)
        print(aplicacion[0].paciente_id)
        usuarioP = Paciente.objects.filter(id=aplicacion[0].paciente_id)[0].user_id
        nombreP = User.objects.filter(id=usuarioP)[0].first_name + " " + User.objects.filter(id=usuarioP)[0].last_name
        datos = {'fecha':str(aplicacion[0].fechaAp), 'nombre': nombreP}
        print(datos)
        paciente = Paciente.objects.filter(id=aplicacion[0].paciente_id)    
        #doc = docx.Document("C:/Users/galil/Documents/GitHub/TT-II/TT/Zeitgeistv3/Especialista/moca.docx")
        nac = str(paciente[0].fechaNac)
        if paciente[0].sexo == 'F':
            sexo = "Femenino"
        else:
            sexo = "Masculino"
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
        print(fecha)
    return render(request, "Especialista/moca-pdf.html",{'datos':datos, 'imagenes':imgs})

def graphic(request):
    if request.method=="POST":
        clave = request.POST.get('clave')
        index = request.POST.get('index')
        paciente = Ap_Screening.objects.filter(cveAcceso=clave)[0].paciente_id
        userP = Paciente.objects.filter(id=paciente)[0].user_id
        nombreP = User.objects.filter(id=userP)[0].first_name + " " + User.objects.filter(id=userP)[0].last_name
        tamizajes = Ap_Screening.objects.filter(paciente=paciente)
        j = 1
        fechas = []
        for t in tamizajes:
            fechas.append(str(t.fechaAp))
        datos = {'nombre': nombreP, 'fecha1':fechas[1], 'fecha2':fechas[0]}
        tam = []
        i = len(tamizajes)
        if index == '2':
            for t in tamizajes:
                clave = i
                aplicaciones = Screening.objects.filter(cveAcceso=t.cveAcceso)
                for tamizaje in aplicaciones:
                    if tamizaje.idReactivo <= 3:
                        dato = {'cat':'vee','nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #visuoespacial/ejecutiva
                        tam.append({'cve': clave, 'datos': dato })                                
                    elif tamizaje.idReactivo == 4:
                        dato = {'cat':'ide','nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #identificacion
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    elif tamizaje.idReactivo == 5:
                        dato = {'cat':'mem','nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #memoria
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    elif 6 <= tamizaje.idReactivo <= 9 :
                        dato = {'cat':'atn', 'nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #atención
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    elif 10 <= tamizaje.idReactivo <= 11:
                        dato = {'cat':'leng','nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #lenguaje
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    elif tamizaje.idReactivo == 12 :
                        dato = {'cat':'abs', 'nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #abstración
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    elif tamizaje.idReactivo == 13 :
                        dato = {'cat':'recd', 'nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #recuerdo diferido
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    elif tamizaje.idReactivo == 14 :
                        dato = {'cat':'ort', 'nReac':tamizaje.idReactivo, 'cal': tamizaje.puntajeReactivo } #orientación
                        #datos.append(dato)
                        tam.append({'cve': clave, 'datos': dato })
                    
                i = i - 1
        #print(tam)
    return render(request, "Especialista/graficas.html",{'datos':datos,'mocas':tam})

