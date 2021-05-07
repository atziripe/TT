from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from Paciente.models import Ap_Screening
from Usuario.models import Paciente
import random
import string
import datetime
import jwt

def inicioEsp(request):
    return render(request, "Especialista/inicioEspecialista.html")

#def editEsp(request):
 #   return render(request, "Especialista/editarEspecialista.html")

def cveAcceso(request, token):
    decodedToken = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
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
            return render(request, "Especialista/inicioEspecialista.html",{"exito": 'false', 'name': decodedToken['first_name'], 'access':token})
        else:
            screening = Ap_Screening.objects.create(cveAcceso=clave, paciente=pacient, fechaAp=fechahoy)
            screening.save()
            print(clave)
            return render(request, "Especialista/inicioEspecialista.html",{'clave':clave, 'name': decodedToken['first_name'], 'access':token })
    return render(request, "Especialista/inicioEspecialista.html", {'name': decodedToken['first_name'], 'access':token})
