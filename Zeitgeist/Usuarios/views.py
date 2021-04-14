from django.http import HttpResponse
from django.shortcuts import render, redirect
from Usuarios.forms import FormLogin #API Forms
from Usuarios.forms import FormRegistroC #API Forms
from Usuarios.forms import FormRegistroP #API Forms
from Usuarios.forms import FormRegistroP #API Forms
from Usuarios.forms import FormRegistroA #API Forms
from Pruebas.models import Paciente
from Cuidador.models import Cuidador
from Especialista.models import Especialista
from Administrador.models import Administrador
from django_cryptography.fields import encrypt
import jwt, json
import re
from datetime import datetime
from django.contrib.auth.models import User

def inicio(request):
    return render(request, "Usuarios/index.html")


def ValidarContrasena(pwd): 
    pass_valida = False
    hay_mayusculas = False
    hay_minusculas = False
    hay_numeros = False

    #Si el tamaño de la contraseña es menor a 8, y no esta compuesta por una combinación de números, letras mayúsculas y minúsculas, no será válida!
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
    user = User.objects.get(username='emm')  #Usuario "owner"
    if request.method=="POST": 
        fregC = FormRegistroC(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if fregC.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',fregC.cleaned_data['correo'].lower()): #Validación de formulario y correo electrónico
                pwd = fregC.cleaned_data['contrasena']
                pwd2 = fregC.cleaned_data['confirmacion_cont']
                nomUser = fregC.cleaned_data['nombreUsuario']

                if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                    return redirect("/registroC/?ya_existe_registro")
                pass_valida = ValidarContrasena(pwd) #Validacion de contraseña:
                if pass_valida == False:
                    return redirect("/registroC/?error_contrasena")
            else:
                return redirect("/registroC/?no_valido")        
	        #Comparar contraseñas
            if pwd == pwd2:
	            #Si son iguales, procedemos a crear nuevo registro:
                nvoC = Cuidador(nomUsuario= nomUser, nombre=fregC.cleaned_data['nombre'], contrasena= pwd, correo=fregC.cleaned_data['correo'], owner= user )
                nvoC.save()
                return redirect("/login/?registro_valido")
            else:
                return redirect("/registroC/?contrasenas_no_coinciden")
        except:
            return redirect("/registroC/?no_valido")
    else:
        fregC=FormRegistroC()
    return render(request, "Usuarios/registroCuidador.html", {"form": fregC}) #Renderizar vista pasando el formulario como contexto


def regP(request):
    if request.method=="POST":
        fregP = FormRegistroP(data=request.POST)
        if fregP.is_valid():
            pwd = fregP.cleaned_data['contrasena']
            pwd2 = fregP.cleaned_data['confirmacion_cont']
        else:
            return redirect("/registroP/?no_valido")
            #print("Por favor introduzca los datos de manera correcta")
	    #Comparar contraseñas
        if pwd == pwd2:
	        #Crear nuevo registro:
            nvoPac = Paciente(nomUsuario= fregP.cleaned_data['nombreUsuario'], especialista= None, cuidador= None,  nombre=fregP.cleaned_data['nombre'], contraseña= pwd, correo=fregP.cleaned_data['correo'], escolaridad=fregP.cleaned_data['escolaridad'], fechaNac= datetime.strptime(fregP.cleaned_data['fechaNac'],'%d/%m/%Y'), sexo=fregP.cleaned_data['sexo'], fechaIng=datetime.date, fechaDiag=datetime.strptime(fregP.cleaned_data['fechaDiag'],'%d/%m/%Y'))
            nvoPac.save()
            return redirect("/login/?registro_valido")
        else:
            return redirect("/registroP/?error_contrasena")
           # print("La contraseña no coincide con su confirmación. Por favor, vuelva a intentarlo.")
           # fregP=FormRegistroP()
    else:
        fregP=FormRegistroP()
    return render(request, "Usuarios/registroPaciente.html", {"form": fregP})

def regA(request):
    #user = User.objects.get(username='emm')  #Usuario "owner"
    if request.method=="POST": 
        fregA = FormRegistroA(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if fregA.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',fregA.cleaned_data['correo'].lower()): #Validación de formulario y correo electrónico
                pwd = fregA.cleaned_data['contrasena']
                pwd2 = fregA.cleaned_data['confirmacion_cont']
                nomUser = fregA.cleaned_data['nombreUsuario']

                if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                    return redirect("/registroA/?ya_existe_registro")
                pass_valida = ValidarContrasena(pwd) #Validacion de contraseña:
                if pass_valida == False:
                    return redirect("/registroA/?error_contrasena")
            else:
                return redirect("/registroA/?no_valido")        
	        #Comparar contraseñas
            if pwd == pwd2:
	            #Si son iguales, procedemos a crear nuevo registro:
                nvoA = Administrador(nomUsuario= nomUser, nombre=fregA.cleaned_data['nombre'], contrasena= pwd, correo=fregA.cleaned_data['correo'])
                nvoA.save()
                return redirect("/login/?registro_valido")
            else:
                return redirect("/registroA/?contrasenas_no_coinciden")
        except:
            return redirect("/registroA/?no_valido")
    else:
        fregA=FormRegistroA()
    return render(request, "Usuarios/registroAdministrador.html", {"form": fregA}) #Renderizar vista pasando el formulario como contexto


def recPasswd(request):
    fRecPass = FormrecuperarPass()
    if request.method == "POST":
        fRecPass = FormrecuperarPass(data = request.POST)
        if fRecPass.is_valid():
            correo = request.POST.get("correo")
            return redirect("/recuperarPass/?valido")
            
    return render(request, "Usuarios/recuperarC.html", {"form": fRecPass})

def ObtenerTipo(user, pwd, tipo):
    if tipo == '1':
        res = Administrador.objects.filter(nomUsuario= user, contrasena = pwd)
    elif tipo == '2':
        res = Cuidador.objects.filter(nomUsuario= user, contrasena = pwd)
    elif tipo == '3':
        res = Especialista.objects.filter(nomUsuario= user, contrasena = pwd)
    else:
        res = Paciente.objects.filter(nomUsuario= user, contrasena = pwd)
    return res

def login(request):
    if request.method=="POST": 
        flogin = FormLogin(data=request.POST)
        if flogin.is_valid():
            user = flogin.cleaned_data['username']
            pwd = flogin.cleaned_data['password']
            tipo = flogin.cleaned_data['tipo']
            if ObtenerTipo(user, pwd, tipo):
                payload = {
                    'id': user,
                    'tipo': tipo,
                }

                jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
                
                #Si el usuario existe, se nos redirige a la página de inicio del tipo de usuario que se ha logeado guardando su nombre:
                if tipo == '1':   
                    nombreCompleto = str(Administrador.objects.all().get(nomUsuario=user).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Administrador/inicioAdministrador.html", {'user': nombre_Especifico, 'token':json.dumps(jwt_token)})
                if tipo == '2':   
                    nombreCompleto = str(Cuidador.objects.all().get(nomUsuario=user).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    #return redirect("../cuidador/", {'user': user, 'token':json.dumps(jwt_token)})
                    return render(request, "Cuidador/inicioCuidador.html", {'user': nombre_Especifico, 'token':json.dumps(jwt_token)})
                if tipo == '3':
                    nombreCompleto = str(Especialista.objects.all().get(nomUsuario=user).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Especialista/inicioEspecialista.html", {'user': nombre_Especifico, 'token':json.dumps(jwt_token)})
                if tipo == '4':
                    nombreCompleto = str(Paciente.objects.all().get(nomUsuario=user).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Paciente/inicioPaciente.html", {'user': nombre_Especifico, 'token':json.dumps(jwt_token)})
                #return render(request, "Usuarios/funciona.html", {'token':json.dumps(jwt_token)})
            else:
                mensaje = "Lo sentimos, no estas en el sistema :("
                return redirect("/login/?no_valido")
    else:
        flogin=FormLogin()
    return render(request, "Usuarios/inicioSesion.html", {"form": flogin})

    
