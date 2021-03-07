from django.db import models
from Cuidador.models import Cuidador

class Especialista(models.Model):
    nomUsuario = models.CharField(primary_key=True, max_length=8)
    nombre = models.CharField(max_length=70)
    contrasena = models.CharField(max_length=50)
    correo = models.EmailField()
    numPacientes = models.IntegerField()
    datos_generales = models.CharField(max_length=200)

class Mensaje(models.Model):
    cveMensaje = models.IntegerField(primary_key=True)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    fechaEnvio = models.DateField
    