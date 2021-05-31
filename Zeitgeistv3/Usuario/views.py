from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.forms import ValidationError
from django.conf import settings
from .forms import FormRegistroC, FormRegistroA, FormRegistroE, FormRegistroP, FormrecuperarPass, FormLogin, FormContacto
from .models import Paciente, Cuidador, Especialista, Administrador
import re, datetime, json, jwt, requests
import datetime 


def inicio(request):
    return render(request, "Usuarios/index.html")


def login(request):
    respuesta = {}
    if request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data["username"]
            contrasena = form.cleaned_data["password"]
            tipo = form.cleaned_data["tipo"]
            payload = {
                'username': usuario,
                'password': contrasena
            }
            response = requests.post('http://localhost:8000/v3/token/', data=json.dumps(
                payload), headers={'content-type': 'application/json'})
            if (response.ok):
                respuesta['access'] = json.loads(response.content)['access']
                respuesta['refresh'] = json.loads(response.content)['refresh']
                decodedPayload = jwt.decode(
                    respuesta['access'], key=settings.SECRET_KEY, algorithms=['HS256'])
                typeuser = requests.get('http://localhost:8000/v1/'+str(tipo)+'user/' + str(
                    decodedPayload['user_id'])+'/', headers={'content-type': 'application/json'})
                if(typeuser.ok):  # if typeuser.stauts_code = 2xx
                    return render(request, ""+tipo+"/inicio"+tipo+".html", {'name': decodedPayload['first_name'],'user_id': decodedPayload['user_id'], 'access': respuesta['access'], 'refresh': respuesta['refresh'], 'tipo': tipo})
                else:
                    return redirect("/login/?404")
            else:
                print(response.json())
                return redirect("/login/?401")
    else:
        form = FormLogin()
    return render(request, "Usuarios/inicioSesion.html", {'form': form, 'respuesta': respuesta})


def ValidarContrasena(pwd):
    pass_valida = False
    hay_mayusculas = False
    hay_minusculas = False
    hay_numeros = False

    # Si el tamaño de la contraseña es menor a 8, y no esta compuesta por una combinación de números, letras mayúsculas y minúsculas, no será válida!
    for caracter in pwd:
        if caracter.isupper():
            hay_mayusculas = True
        if caracter.islower():
            hay_minusculas = True
        if caracter.isdigit():
            hay_numeros = True

    if len(pwd) > 7 and hay_mayusculas and hay_minusculas and hay_numeros:
        pass_valida = True
    return pass_valida


def regC(request):
    base = "Usuarios/baseIndex.html"
    if request.method == "POST":
        fregC = FormRegistroC(data=request.POST)
        try:  # En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            # Validación de formulario y correo electrónico
            if fregC.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', fregC.cleaned_data['correo'].lower()):
                pwd = fregC.cleaned_data['contrasena']
                pwd2 = fregC.cleaned_data['confirmacion_cont']
                if pwd == pwd2:
                    if ValidarContrasena(pwd):
                        payload = {
                            'username': fregC.cleaned_data['nombreUsuario'],
                            'password': pwd,
                            'email': fregC.cleaned_data['correo'],
                            'first_name': fregC.cleaned_data['nombre'],
                            'last_name': fregC.cleaned_data['apellidos']
                        }
                        response = requests.post('http://127.0.0.1:8000/v1/createuser/', data=json.dumps(
                            payload), headers={'content-type': 'application/json'})
                        print(response.json())
                        if(response.ok):
                            payload = {
                                "user": json.loads(response.content)['id']
                            }
                            registerC = requests.post('http://127.0.0.1:8000/v1/createcare/', data=json.dumps(
                            payload), headers={'content-type': 'application/json'})
                            if(registerC.ok):
                                grupo = Group.objects.get(name='Cuidadores') 
                                grupo.user_set.add(json.loads(response.content)['id'])
                                print("Se pudo registrar")
                                return redirect("/login/?registro_valido")
                            else:
                                print(registerC.status_code)
                                print("No se pudo hacer el registro del cuidador")
                        else:
                            print(response.status_code)
                            print("No se pudo hacer el registro del usuario")
                            return redirect("/registroC/?ya_existe_registro")
                    else:
                        # Contraseña invalida
                        return redirect("/registroC/?pwdinvalid")
                else:
                    # Passwords no iguales
                    return redirect("/registroC/?pwdns")
        except:
            return redirect("/registroC/?no_valido")
    else:
        fregC = FormRegistroC()
    return render(request, "Usuarios/registroCuidador.html", {"form": fregC, "base" : base})
            

def regE(request):
    base = "Usuarios/baseIndex.html"
    if request.method == "POST":
        fregE = FormRegistroE(data=request.POST)
        try:
           # Validación de formulario y correo electrónico
            if fregE.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', fregE.cleaned_data['correo'].lower()):
                pwd = fregE.cleaned_data['contrasena']
                pwd2 = fregE.cleaned_data['confirmacion_cont']
                cedula = fregE.cleaned_data['nombreUsuario'].replace(" ","")
                
                consulta_cp = requests.get('https://api.allorigins.win/get?&url=https%3A//www.cedulaprofesional.sep.gob.mx/cedula/buscaCedulaJson.action%3Fjson%3D%257B%2522maxResult%2522%253A%252250%2522%252C%2522nombre%2522%253A%2522%2522%252C%2522paterno%2522%253A%2522%2522%252C%2522materno%2522%253A%2522%2522%252C%2522idCedula%2522%253A%2522+'+cedula+'+%2522%257D%26wt%3Djson&callback=&charset=utf-8')
                if(consulta_cp.ok):
                    res = json.loads(consulta_cp.content)['contents']
                    titulo = res[res.find("titulo")+9:res.find('filename')-5]
                    print(titulo)
                    if titulo.find("INTERN") != -1 or titulo.find("GERIATR") != -1:
                        print(titulo.find("INTERN") or titulo.find("GERIATR"))
                        if pwd == pwd2:
                            if ValidarContrasena(pwd):
                                payload = {
                                    'username': cedula,
                                    'password': pwd,
                                    'email': fregE.cleaned_data['correo'],
                                    'first_name': fregE.cleaned_data['nombre'],
                                    'last_name': fregE.cleaned_data['apellidos']
                                }
                                response = requests.post('http://127.0.0.1:8000/v1/createuser/', data=json.dumps(
                                    payload), headers={'content-type': 'application/json'})
                                print(response.json())
                                if(response.ok):
                                    payload = {
                                        'user': json.loads(response.content)['id'],
                                        'numPacientes': fregE.cleaned_data['numPacientes'],
                                        'datos_generales': fregE.cleaned_data['datos_generales']
                                    }
                                    registerE = requests.post('http://127.0.0.1:8000/v1/createspecialist/', data=json.dumps(
                                    payload), headers={'content-type': 'application/json'})
                                    if(registerE.ok):
                                        grupo = Group.objects.get(name='Especialistas') 
                                        grupo.user_set.add(json.loads(response.content)['id'])
                                        print("Se pudo registrar")
                                        return redirect("/login/?registro_valido")
                                    else:
                                        print(registerE.status_code)
                                        print("No se pudo hacer el registro del especialista")
                                else:
                                    print(response.status_code)
                                    print("No se pudo hacer el registro del usuario")
                            else:
                                # Contraseña invalida
                                return redirect("/registroE/?pwdinvalid")
                        else:
                            print(response.status_code)
                            print("No se pudo hacer el registro del usuario")
                            return redirect("/registroE/?ya_existe_registro")
                    else:
                        return redirect("/registroE/?cpincorrecta")
                else:
                    print(consulta_cp.status_code)
                    return redirect("/registroE/?cperror")
        except:
            return redirect("/registroE/?no_valido")
    else:
        fregE = FormRegistroE()
    # Renderizar vista pasando el formulario como contexto
    return render(request, "Usuarios/registroEspecialista.html", {"form": fregE, "base": base})


def regP(request):
    base = "Usuarios/baseIndex.html"
    if request.method == "POST":
        fregP = FormRegistroP(data=request.POST)
        if fregP.is_valid():
            if fregP.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', fregP.cleaned_data['correo'].lower()):
                pwd = fregP.cleaned_data['contrasena']
                pwd2 = fregP.cleaned_data['confirmacion_cont']
                fechaNac = fregP.cleaned_data['fechaNac']
                fechaDiag = fregP.cleaned_data['fechaDiag']
                fecha = datetime.date.today()
                año_TerceraEdad = int(fecha.year) - 60

                if fechaNac < fecha and fechaNac < fechaDiag:
                    if fechaDiag > fecha:
                        return redirect("/registroP/?fechaDiag_mayor_fechaIng")
                                #La fecha de diagnóstico debe ser anterior a la fecha en la que se hace el registro.
                    if fechaDiag.year< 1890 or fechaNac.year < 1890:
                            #raise ValidationError("La fecha de diagnostico y fecha de nacimiento no pueden registrarse en el día que usted indica, por favor compruebe las fechas y vuelva a escribirlas. Asegúrese de escribir un año mayor a 1890 y que las fechas no sobrepasen a la fecha actual.")
                            #print ("Fechas no Validas")
                        return redirect("/registroP/?fechas_no_validas")
                            # La fecha de diagnostico y fecha de nacimiento no pueden registrarse en el día que usted indica, por favor compruebe las fechas y vuelva a escribirlas. Asegúrese de escribir un año mayor a 1890 y que las fechas no sobrepasen a la fecha actual.
                    if fechaNac.year > año_TerceraEdad:
                        return redirect("/registroP/?fechaNac_Paciente")
                else:
                    return redirect("/registroP/?fechas_no_validas")

                fechaNac_str = str(fechaNac)
                fechaDiag_str = str(fechaDiag)

                if pwd == pwd2:
                    payload = {
                        'username': fregP.cleaned_data['nombreUsuario'],
                        'password': pwd,
                        'email': fregP.cleaned_data['correo'],
                        'first_name': fregP.cleaned_data['nombre'],
                        'last_name': fregP.cleaned_data['apellidos']
                    }
                    response = requests.post('http://127.0.0.1:8000/v1/createuser/', data=json.dumps(
                        payload), headers={'content-type': 'application/json'})
                    if(response.ok):
                        payloadP = {
                            'user': json.loads(response.content)['id'],
                            'sexo': fregP.cleaned_data['sexo'],
                            'escolaridad': fregP.cleaned_data['escolaridad'],
                            'fechaNac': fechaNac_str,
                            'fechaDiag': fechaDiag_str
                        }
                        registerC = requests.post('http://127.0.0.1:8000/v1/createpacient/', data=json.dumps(payloadP), headers={'content-type': 'application/json'})
                        if(registerC.ok):
                            grupo = Group.objects.get(name='Pacientes') 
                            grupo.user_set.add(json.loads(response.content)['id'])
                            print("Se pudo registrar")
                            return redirect("/login/?registro_valido")
                        else:
                            print(registerC.status_code)
                            return redirect("/registroP/?no_valido")
                    else:
                        print(response.status_code)
                        return redirect("/registroP/?ya_existe_registro")
                else:
                    print("contraseña no igual")
                    # Passwords no iguales
                    return redirect("/registroP/?pwdns")
        #except:
         #   print("no se hizo el registro")
          #  return redirect("/registroP/?no_valido")
    else:
        fregP = FormRegistroP()
    return render(request, "Usuarios/registroPaciente.html", {"form": fregP, "base": base})


def regA(request, token, tipo, name):
    base = "Administrador/baseAdministrador.html"
    if request.method == "POST":
        fregA = FormRegistroA(data=request.POST)
        try:  # En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            # Validación de formulario y correo electrónico
            if fregA.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', fregA.cleaned_data['correo'].lower()):
                pwd = fregA.cleaned_data['contrasena']
                pwd2 = fregA.cleaned_data['confirmacion_cont']
                if pwd == pwd2:
                    if ValidarContrasena(pwd):
                        payload = {
                            'username': fregA.cleaned_data['nombreUsuario'],
                            'password': pwd,
                            'email': fregA.cleaned_data['correo'],
                            'first_name': fregA.cleaned_data['nombre'],
                            'last_name': fregA.cleaned_data['apellidos']
                        }
                        response = requests.post('http://127.0.0.1:8000/v1/createuser/', data=json.dumps(
                            payload), headers={'content-type': 'application/json', 'Authorization': 'Bearer '+ token})
                        print(response.json())
                        if(response.ok):
                            payload = {
                                "user": json.loads(response.content)['id']
                            }
                            registerA = requests.post('http://127.0.0.1:8000/v1/createadmin/', data=json.dumps(
                            payload), headers={'content-type': 'application/json', 'Authorization': 'Bearer '+ token})
                            if(registerA.ok):
                                grupo = Group.objects.get(name='Administradores') 
                                grupo.user_set.add(json.loads(response.content)['id'])
                                print("Se pudo registrar")
                                return render(request, "Administrador/inicioAdministrador.html", {"name": name, "access": token, "tipo": tipo, "AdminRegistration_Successful": True})
                            else:
                                print(registerA.status_code)
                                print("No se pudo hacer el registro del administrador")
                        else:
                            print(response.status_code)
                            print("No se pudo hacer el registro del usuario")
                            return render(request, "Usuarios/registroAdministrador.html", {"name": name, "form": fregA, "access": token, "tipo": tipo, "already_exists": True, "base": base})
                    else:
                        # Contraseña invalida
                        return render(request, "Usuarios/registroAdministrador.html", {"name": name, "form": fregA, "access": token, "tipo": tipo, "invalid_pwd": True, "base": base})
                else:
                    # Passwords no iguales
                    return render(request, "Usuarios/registroAdministrador.html", {"name": name, "form": fregA, "access": token, "tipo": tipo, "No_match_pwds": True, "base": base})
        except:
            return render(request, "Usuarios/registroAdministrador.html", {"name": name, "form": fregA, "access": token, "tipo": tipo, "invalid_reg": True, "base": base})
    else:
        fregA = FormRegistroA()
    # Renderizar vista pasando el formulario como contexto
    return render(request, "Usuarios/registroAdministrador.html", {"name": name, "form": fregA, "tipo": tipo, "base": base, "access": token})

def recPassConfirm(request):
    return render(request, "Usuarios/resetPwd/resetPwdConfirm.html")
                
def cambiarPasswd(request, iduser, token, tipo, name):
    base = str( tipo + "/base" + tipo+".html")
    print(base)
    if request.method == "POST":
        try: 
            pwd_a = request.POST['pwdactual']
            pwd_n = request.POST['pwdnueva']
            pwd_n2 = request.POST['pwdnueva2']
            
            if pwd_n == pwd_n2:
                if ValidarContrasena(pwd_n) or tipo == "Paciente": #El paciente no tiene restriccion en la contraseña
                    payload = {
                        "old_password": pwd_a,    
                        "password": pwd_n,    
                        "password2": pwd_n2
                    }
                    response = requests.put('http://127.0.0.1:8000/v3/cambiarpwd/'+str(iduser)+'/', data=json.dumps(
                        payload), headers={'content-type': 'application/json', 'Authorization': 'Bearer '+ token})
                    if(response.ok):
                        return redirect("/login/?changevalid") #Se cambia la contraseña y se vuelve a loguear
                    else:
                        print(response.status_code)
                        print(response.json())
                        return render(request, ""+tipo+"/inicio"+tipo+".html", {'name': name, 'user_id': iduser, 'access': token, 'tipo': tipo, 'base': base, 'invalid': True})                      
                else:
                    print("contraseña invalida")
                    # Contraseña invalida
                    return render(request, ""+tipo+"/inicio"+tipo+".html", {"name": name, 'user_id': iduser, 'access': token, 'tipo': tipo, 'base': base, 'pwd_invalid': True})
            else:
                print("contraseña no igual")
                # Passwords no iguales
                return render(request, ""+tipo+"/inicio"+tipo+".html", {"name": name, 'user_id': iduser, 'access': token, 'tipo': tipo, 'base': base, 'no_match_pdws': True})
        except:
            print("no se hizo el cambio")
            print(response.json())
            return render(request, ""+tipo+"/inicio"+tipo+".html", {'name': name, 'user_id': iduser, 'access': token, 'tipo': tipo, 'base': base, 'invalid': True})                      
    # Cualquier error redirecciona a la pagina de inicio del usuario, si no hay errores, se manda al login para acceder de nuevo.

    return render(request, tipo+"/inicio"+tipo+".html", {"name": name, 'user_id': iduser, 'access': token, 'tipo': tipo, 'base' : base})
    

def Contacto(request):
    #try:
    a=0
    if a ==0:
        fContacto = FormContacto()
        if request.method == "POST":
            fContacto = FormContacto(data=request.POST)
            if fContacto.is_valid():
                nombre = request.POST.get("nombre")
                mensaje = request.POST.get("mensaje")
                return redirect("/contacto/?valido")
        else:
            return render(request, "Usuarios/Contacto.html", {'form': fContacto})
    #except:
    #    return render(request, "Usuarios/index.html")