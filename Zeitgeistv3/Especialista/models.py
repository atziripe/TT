from django.db import models
from Usuario.models import Especialista, Cuidador

# Create your models here.

class Mensaje(models.Model):
    cveMensaje = models.AutoField(auto_created = True, primary_key=True)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    fechaEnvio = models.DateField()
    