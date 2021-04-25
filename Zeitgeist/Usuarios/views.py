from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FormLogin, FormrecuperarPass, FormRegistroA, FormRegistroC, FormRegistroE, FormRegistroP
from Pruebas.models import Paciente
from Cuidador.models import Cuidador
from Especialista.models import Especialista
from Administrador.models import Administrador
from django_cryptography.fields import encrypt
import jwt, json
import re
import datetime 
from django.contrib.auth.models import User
from django.forms import ValidationError
from Pruebas.views import inicioPa
from Especialista.views import inicioEsp
from Cuidador.views import inicioC
from Administrador.views import inicioA


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

def regE(request):
    user = User.objects.get(username='emm')  #Usuario "owner"
    if request.method=="POST": 
        fregE = FormRegistroE(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if fregE.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',fregE.cleaned_data['correo'].lower()): #Validación de formulario y correo electrónico
                pwd = fregE.cleaned_data['contrasena']
                pwd2 = fregE.cleaned_data['confirmacion_cont']
                nomUser = fregE.cleaned_data['nombreUsuario']

                if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                    return redirect("/registroE/?ya_existe_registro")
                pass_valida = ValidarContrasena(pwd) #Validacion de contraseña:
                if pass_valida == False:
                    return redirect("/registroE/?error_contrasena")
            else:
                return redirect("/registroE/?no_valido")        
	        #Comparar contraseñas
            if pwd == pwd2:
	            #Si son iguales, procedemos a crear nuevo registro:
                nvoE = Especialista(nomUsuario= nomUser, nombre=fregE.cleaned_data['nombre'], contrasena= pwd, correo=fregE.cleaned_data['correo'], numPacientes=2, datos_generales=fregE.cleaned_data['datos_generales'])
                nvoE.save()
                return redirect("/login/?registro_valido")
            else:
                return redirect("/registroE/?contrasenas_no_coinciden")
        except:
            return redirect("/registroE/?no_valido")
    else:
        fregE=FormRegistroE()
    return render(request, "Usuarios/registroEspecialista.html", {"form": fregE}) #Renderizar vista pasando el formulario como contexto


def regP(request):
    #user = User.objects.get(username='emm')  #Usuario "owner"
    if request.method=="POST": 
        fregP = FormRegistroP(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if fregP.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',fregP.cleaned_data['correo'].lower()): #Validación de formulario y correo electrónico   
                pwd = fregP.cleaned_data['contrasena']
                pwd2 = fregP.cleaned_data['confirmacion_cont']
                nomUser = fregP.cleaned_data['nombreUsuario']
                fecha = datetime.date.today()
                fechaHoy = str(fecha.year)+"-"+str(fecha.month)+"-"+str(fecha.day)
                fechaDiag = fregP.cleaned_data['fechaDiag']
                fechaNac = fregP.cleaned_data['fechaNac']

                if fechaNac < fecha and fechaNac < fechaDiag:
                    if fechaDiag > fecha:
                        return redirect("/registroP/?fechaDiag_mayor_fechaIng")
                                #La fecha de diagnóstico debe ser anterior a la fecha en la que se hace el registro.
                    if fechaDiag.year < 1890 or fechaNac.year < 1890:
                            #raise ValidationError("La fecha de diagnostico y fecha de nacimiento no pueden registrarse en el día que usted indica, por favor compruebe las fechas y vuelva a escribirlas. Asegúrese de escribir un año mayor a 1890 y que las fechas no sobrepasen a la fecha actual.")
                            #print ("Fechas no Validas")
                        return redirect("/registroP/?fechas_no_validas")
                            # La fecha de diagnostico y fecha de nacimiento no pueden registrarse en el día que usted indica, por favor compruebe las fechas y vuelva a escribirlas. Asegúrese de escribir un año mayor a 1890 y que las fechas no sobrepasen a la fecha actual.
                else:
                    return redirect("/registroP/?fechas_no_validas")

                if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                    return redirect("/registroP/?ya_existe_registro")
                    #Este usuario no tiene validacion de contraseña!
                    
            else:
                return redirect("/registroP/?no_valido")        
    	        #Comparar contraseñas
            if pwd == pwd2:
    	            #Si son iguales, procedemos a crear nuevo registro:
                nvoP = Paciente(nomUsuario= fregP.cleaned_data['nombreUsuario'], especialista= None, cuidador= None,  nombre=fregP.cleaned_data['nombre'], contrasena= pwd, correo=fregP.cleaned_data['correo'], escolaridad=fregP.cleaned_data['escolaridad'], fechaNac= fechaNac, sexo=fregP.cleaned_data['sexo'], fechaIng=fechaHoy, fechaDiag=fechaDiag)
                nvoP.save()
                return redirect("/login/?registro_valido")
            else:
                return redirect("/registroP/?contrasenas_no_coinciden")
        except:
            return redirect("/registroP/?no_valido")
    else:
        fregP=FormRegistroP()
    return render(request, "Usuarios/registroPaciente.html", {"form": fregP}) #Renderizar vista pasando el formulario como contexto


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
    #Cerrando sesion anterior:
    if request.session.get("usuarioActual") != None:
        print("Se ha cerrado la sesión de "+ request.session.get("usuarioActual"))
        del request.session["usuarioActual"]
    #Aqui ya procedemos a establecer nueva sesión:
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
                
                request.session["usuarioActual"] = user #Creamos sesión
                print("Inicio de sesión como: "+ request.session.get("usuarioActual"))

                #Si el usuario existe, se nos redirige a la página de inicio del tipo de usuario que se ha logeado guardando su nombre:
                if tipo == '1':   
                    AdminActual = request.session.get("usuarioActual")
                    nombreCompleto = str(Administrador.objects.all().get(nomUsuario=AdminActual).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Administrador/inicioAdministrador.html",{'user': AdminActual, 'nombre': nombre_Especifico})
  
                if tipo == '2':   
                    cuidadorActual = request.session.get("usuarioActual")
                    nombreCompleto = str(Cuidador.objects.all().get(nomUsuario=cuidadorActual).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Cuidador/inicioCuidador.html", {'user': cuidadorActual, 'nombre': nombre_Especifico})

                if tipo == '3':
                    doctorActual = request.session.get("usuarioActual")
                    nombreCompleto = str(Especialista.objects.all().get(nomUsuario=doctorActual).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Especialista/inicioEspecialista.html", {'user': doctorActual, 'nombre': nombre_Especifico})

                if tipo == '4':
                    pacienteActual = request.session.get("usuarioActual")
                    nombreCompleto = str(Paciente.objects.all().get(nomUsuario=pacienteActual).nombre).split()
                    nombre_Especifico = nombreCompleto[0]
                    return render(request, "Pruebas/inicioPaciente.html", {'user': pacienteActual, 'nombre': nombre_Especifico})
       
                    
                    #return render(request, "", {'user', 'token':json.dumps(jwt_token)})
            else:
                return redirect("/login/?no_valido")
    else:
        flogin=FormLogin()
    return render(request, "Usuarios/inicioSesion.html", {"form": flogin})