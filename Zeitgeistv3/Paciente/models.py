from django.db import models
from Usuario.models import Especialista, Cuidador, Paciente
from Cuidador.models import Pregunta

class Ap_Reminiscencia(models.Model):
    cveAcceso = models.CharField(primary_key=True, max_length=15)
    #reminiscencia = models.ManyToManyField('Pregunta', through='Reminiscencia')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField(null=True)

class Reminiscencia(models.Model):
    idApp = models.CharField(primary_key=True, max_length=17)
    cveAcceso = models.ForeignKey(Ap_Reminiscencia, related_name='idRem', on_delete=models.CASCADE)
    idPregunta = models.ForeignKey(Pregunta, related_name='idRem', on_delete=models.CASCADE, null=True)
    respuestaPaciente = models.CharField(max_length=255)
    valoracion = models.BooleanField()

class Ap_Screening(models.Model):
    cveAcceso = models.CharField(primary_key=True, max_length=10)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField()

class Screening(models.Model):
    idReactivo = models.IntegerField(primary_key=True)
    cveAcceso = models.ForeignKey(Ap_Screening, on_delete=models.CASCADE, null=True)
    respuestaT = models.CharField(max_length=255)
    respuestaImg = models.ImageField()
    puntajeReactivo = models.IntegerField()
    puntajeMaximo = models.IntegerField()

    class Meta:
        unique_together = (('cveAcceso', 'idReactivo'),)


class Tema(models.Model):
    DIFICULTAD=[
        ('F',"Facil"),
        ('M', "Medio"),
        ('D', "Dificil"),
    ]
    cveTemas = models.IntegerField(primary_key=True)
    tema = models.CharField(max_length=20)
    dificultad = models.CharField(choices=DIFICULTAD, max_length=50)

class Ent_Cogn(models.Model):
    STATUS = [
        ('S',"Superado"),
        ('NS',"No superado")
    ]
    cveAcceso = models.CharField(max_length=10, primary_key=True)
    cveTema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField
    estado =  models.CharField(choices=STATUS, max_length=50)
    tiempo = models.TimeField

class Palabra(models.Model):
    cvePalabra = models.IntegerField(primary_key=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    palabra = models.CharField(max_length=10)

    class Meta: 
        unique_together = (('cvePalabra', 'tema'),)