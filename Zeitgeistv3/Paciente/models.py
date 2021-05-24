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
    cveAcceso = models.CharField(primary_key=True, max_length=18)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField(null=True)

class Screening(models.Model):
    idApp = models.CharField(primary_key=True, max_length=18)
    idReactivo = models.IntegerField()
    cveAcceso = models.ForeignKey(Ap_Screening, on_delete=models.CASCADE, null=True)
    respuestaT = models.CharField(max_length=255, null = True)
    respuestaImg = models.ImageField(upload_to= "screening", null=True, blank=True)
    puntajeReactivo = models.IntegerField()
    puntajeMaximo = models.IntegerField()

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
    cveAcceso = models.CharField(max_length=18, primary_key=True)
    cveTema = models.ForeignKey(Tema, on_delete=models.CASCADE, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    estado =  models.CharField(choices=STATUS, max_length=50)
    tiempo = models.TimeField(null=True)

class Palabra(models.Model):
    idPalabra = models.CharField(primary_key=True, max_length=10)
    cvePalabra = models.IntegerField()
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    palabra = models.CharField(max_length=10)
