from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.forms import ValidationError
from django.conf import settings
from .forms import FormRegistroC, FormRegistroA, FormRegistroE, FormRegistroP, FormrecuperarPass, FormLogin
from .models import Paciente, Cuidador, Especialista, Administrador
import re
import datetime
import json
import jwt
import requests


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
                    return render(request, ""+tipo+"/inicio"+tipo+".html", {'user': decodedPayload['first_name'], 'token': respuesta})
                else:
                    return redirect("/login/?404")
            else:
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
    if request.method == "POST":
        fregC = FormRegistroC(data=request.POST)
        try:  # En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            # Validación de formulario y correo electrónico
            if fregC.is_valid():
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
    return render(request, "Usuarios/registroCuidador.html", {"form": fregC})


def regE(request):
    user = User.objects.get(username='emm')  # Usuario "owner"
    if request.method == "POST":
        fregE = FormRegistroE(data=request.POST)
        try:
            if fregE.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', fregE.cleaned_data['correo'].lower()):
                pwd = fregE.cleaned_data['contrasena']
                pwd2 = fregE.cleaned_data['confirmacion_cont']
                nomUser = fregE.cleaned_data['nombreUsuario']

                # Validación de que usuario no existe anteriormente:
                if Cuidador.objects.filter(nomUsuario=nomUser) or Administrador.objects.filter(nomUsuario=nomUser) or Paciente.objects.filter(nomUsuario=nomUser) or Especialista.objects.filter(nomUsuario=nomUser):
                    return redirect("/registroE/?ya_existe_registro")
                # Validacion de contraseña:
                pass_valida = ValidarContrasena(pwd)
                if pass_valida == False:
                    return redirect("/registroE/?error_contrasena")
            else:
                return redirect("/registroE/?no_valido")
                # Comparar contraseñas
            if pwd == pwd2:
                # Si son iguales, procedemos a crear nuevo registro:
                nvoE = Especialista(nomUsuario=nomUser, nombre=fregE.cleaned_data['nombre'], contrasena=pwd,
                                    correo=fregE.cleaned_data['correo'], numPacientes=2, datos_generales=fregE.cleaned_data['datos_generales'])
                nvoE.save()
                return redirect("/login/?registro_valido")
            else:
                return redirect("/registroE/?contrasenas_no_coinciden")
        except:
            return redirect("/registroE/?no_valido")
    else:
        fregE = FormRegistroE()
    # Renderizar vista pasando el formulario como contexto
    return render(request, "Usuarios/registroEspecialista.html", {"form": fregE})


def regP(request):
    if request.method == "POST":
        fregP = FormRegistroP(data=request.POST)
        try:
            if fregP.is_valid():
                pwd = fregP.cleaned_data['contrasena']
                pwd2 = fregP.cleaned_data['confirmacion_cont']
                if pwd == pwd2:
                    if ValidarContrasena(pwd):
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
                                'fechaNac': fregP.cleaned_data['fechaNac'],
                                'fechaDiag': fregP.cleaned_data['fechaDiag']
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
                            return redirect("/registroP/?no_valido")
                            
                    else:
                        print("conraseña invalida")
                        # Contraseña invalida
                        return redirect("/registroP/?pwdinvalid")
                else:
                    print("conraseña no igual")
                    # Passwords no iguales
                    return redirect("/registroP/?pwdns")
        except:
            print("no se hizo el registro")
            return redirect("/registroP/?no_valido")
    else:
        fregP = FormRegistroP()
    return render(request, "Usuarios/registroPaciente.html", {"form": fregP})

def regA(request):
    # user = User.objects.get(username='emm')  #Usuario "owner"
    if request.method == "POST":
        fregA = FormRegistroA(data=request.POST)
        try:  # En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            # Validación de formulario y correo electrónico
            if fregA.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', fregA.cleaned_data['correo'].lower()):
                pwd = fregA.cleaned_data['contrasena']
                pwd2 = fregA.cleaned_data['confirmacion_cont']
                nomUser = fregA.cleaned_data['nombreUsuario']

                # Validación de que usuario no existe anteriormente:
                if Cuidador.objects.filter(nomUsuario=nomUser) or Administrador.objects.filter(nomUsuario=nomUser) or Paciente.objects.filter(nomUsuario=nomUser) or Especialista.objects.filter(nomUsuario=nomUser):
                    return redirect("/registroA/?ya_existe_registro")
                # Validacion de contraseña:
                pass_valida = ValidarContrasena(pwd)
                if pass_valida == False:
                    return redirect("/registroA/?error_contrasena")
            else:
                return redirect("/registroA/?no_valido")
                # Comparar contraseñas
            if pwd == pwd2:
                # Si son iguales, procedemos a crear nuevo registro:
                nvoA = Administrador(
                    nomUsuario=nomUser, nombre=fregA.cleaned_data['nombre'], contrasena=pwd, correo=fregA.cleaned_data['correo'])
                nvoA.save()
                return redirect("/login/?registro_valido")
            else:
                return redirect("/registroA/?contrasenas_no_coinciden")
        except:
            return redirect("/registroA/?no_valido")
    else:
        fregA = FormRegistroA()
    # Renderizar vista pasando el formulario como contexto
    return render(request, "Usuarios/registroAdministrador.html", {"form": fregA})


def recPasswd(request):
    fRecPass = FormrecuperarPass()
    if request.method == "POST":
        fRecPass = FormrecuperarPass(data=request.POST)
        if fRecPass.is_valid():
            correo = request.POST.get("correo")
            return redirect("/recuperarPass/?valido")
