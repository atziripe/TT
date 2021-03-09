from django.db import models
from Cuidador.models import Cuidador
from Usuarios.models import Usuario
class Especialista(models.Model):
    nomUsuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, primary_key=True)
    numPacientes = models.IntegerField()
    datos_generales = models.CharField(max_length=200)

class Mensaje(models.Model):
    cveMensaje = models.IntegerField(primary_key=True)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    fechaEnvio = models.DateField
    