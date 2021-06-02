from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Especialista
from Usuarios import views
from .forms import FormEditarE
import re

# Create your views here.

def inicioEsp(request):
    return render(request, "Usuarios/index.html")

def editE(request):
    base = "Especialista/baseEspecialista.html" #Para la base de edicion necesitamos tener el menu del perfil que estamos editando
    especialistaActual = Especialista.objects.get(nomUsuario= request.session.get("usuarioActual"))

    if request.method=="POST": 
        feditE = FormEditarE(data=request.POST)
        try:        #En caso de un error como exceder el maximo de letras de un campo, mandamos una excepcion:
            if feditE.is_valid() and re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',request.POST['nvo_correo'].lower()): #Validación de formulario y correo electrónico
                pwd = request.POST['nvo_contrasena']
                curr_pwd = request.POST['confirmacion_cont']
                nomUser = request.POST['nvo_nombreUsuario']

                if nomUser != especialistaActual.nomUsuario: #Si el nombre de usuario no se modifico, nos saltamos validación de existencia.
                    if Cuidador.objects.filter(nomUsuario= nomUser) or Administrador.objects.filter(nomUsuario= nomUser) or Paciente.objects.filter(nomUsuario= nomUser) or Especialista.objects.filter(nomUsuario = nomUser): #Validación de que usuario no existe anteriormente:
                        return redirect("/especialista/editarE/?ya_existe_registro")
                
                pass_valida = views.ValidarContrasena(pwd) #Validacion de contraseña:
                if pass_valida == False:
                    return redirect("/especialista/editarE/?contrasena_invalida")
            else:
                return redirect("/especialista/editarE/?no_valido")        
	        #Checar que contraseña actual es correcta
            if curr_pwd == especialistaActual.contrasena:
	            #Si coincide, se aplica el cambio solicitado

                especialistaActual.nomUsuario = nomUser
                especialistaActual.nombre=request.POST['nvo_nombre']
                especialistaActual.contrasena= pwd
                especialistaActual.correo=request.POST['nvo_correo']
                especialistaActual.datos_generales=request.POST['nvos_datos_generales']
                especialistaActual.numPacientes = request.POST['nvo_numPacientes']
                especialistaActual.save()

                return redirect("/login/?edicion_valida")
            else:
                return redirect("/especialista/editarE/?error_contrasena")
        except:
            return redirect("/especialista/editarE/?no_valido")
    else:
        feditE=FormEditarE()
    return render(request, "Especialista/editarEspecialista.html", {"form": feditE, "base": base}) #Renderizar vista pasando el formulario como contexto
