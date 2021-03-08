from django.db import models
from Especialista.models import Especialista
from Cuidador.models import Cuidador

class Paciente(models.Model):
    ESCOLARIDAD = [
        ('N','Ninguna'),
        ('PR','Primaria'),
        ('SC','Secundaria'),
        ('BCH','Bachillerato'),
        ('SUP','Licenciatura o superior'),
    ]
    GENDER = [
        ('F', "Femenino"),
        ('M', "Masculino"),
    ]
    nomUsuario = models.CharField(primary_key=True,max_length=20)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=70)
    contraseña = models.CharField(max_length=50)
    correo = models.EmailField(blank=True)
    escolaridad = models.CharField(choices=ESCOLARIDAD, max_length=50)
    fechaNac = models.DateField()
    sexo = models.CharField(choices=GENDER, max_length=50)
    fechaIng = models.DateField()
    fechaDiag = models.DateField()


class Pregunta(models.Model):
    TIPO = [
        ('TXT', 'Texto'),
        ('IMG', 'Imagen'),
        ('AUD', 'Audio'),
    ]
    idReactivo = models.IntegerField(primary_key=True)
    pregunta = models.TextField()
    tipo = models.CharField(choices=TIPO,max_length=50)
    preguntaBin = models.BooleanField()

class Ap_Reminiscencia(models.Model):
    cveAcceso = models.CharField(primary_key=True, max_length=10)
    reminiscencia = models.ManyToManyField('Pregunta', through='Reminiscencia', related_name='aps')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField()

class Reminiscencia(models.Model):
    cveAcceso = models.ForeignKey(Ap_Reminiscencia, related_name='idRem', on_delete=models.CASCADE)
    idReactivo = models.ForeignKey(Pregunta, related_name='idRem', on_delete=models.CASCADE)
    respuestaPaciente = models.CharField(max_length=255)
    respuestaCuidador = models.CharField(max_length=255)
    resultado = models.IntegerField()
    unique_together = [['cveAcceso', 'idReactivo']]

class Ap_Screening(models.Model):
    cveAcceso = models.CharField(primary_key=True, max_length=10)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField()

class Screening(models.Model):
    idReactivo = models.IntegerField()
    cveAcceso = models.ForeignKey( Ap_Reminiscencia, on_delete=models.CASCADE)
    respuestaT = models.CharField(max_length=100)
    respuestaImg = models.ImageField()
    puntajeReactivo = models.IntegerField()
    puntajeMaximo = models.IntegerField()
    unique_together = (('idReactivo', 'cveAcceso'))
    

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
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    cvePalabra = models.IntegerField(primary_key=True)
    palabra = models.CharField(max_length=10)
    unique_together = (('tema', ' cvePalabra'))