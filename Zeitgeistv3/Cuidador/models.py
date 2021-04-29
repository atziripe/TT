from django.db import models
from Usuario.models import Cuidador

# Create your models here.



class Cat_Pregunta(models.Model):
    TIPODATO = [
        ('TXT', 'Texto'),
        ('IMG', 'Imagen'),
        ('AUD', 'Audio'),
    ]
    TIPO = [
        ('A', 'Abierta'),
        ('OP', 'Opcion Multiple'),
    ]
    idReactivo = models.IntegerField(primary_key=True)
    reactivo = models.TextField()
    tipoDato = models.CharField(choices=TIPODATO,max_length=50)
    tipoPregunta = models.CharField(choices=TIPO, max_length=20)
    
    def __str__(self):
        return str(self.idReactivo)

class Pregunta(models.Model):
    idReactivo = models.ForeignKey(Cat_Pregunta, on_delete=models.CASCADE)
    idCuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to= "reminiscencia", null=True, blank=True)
    audio = models.FileField(upload_to= "reminiscencia", null=True, blank=True)
    respuestaCuidador = models.CharField(max_length=255)

