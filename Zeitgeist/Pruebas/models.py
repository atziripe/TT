from django.db import models

class Cuidador(models.Model):
    nomUsuario = models.CharField(primary_key = True, max_length=20)
    nombre = models.CharField(max_length=70)
    contraseña = models.CharField(max_length=45)
    correo = models.EmailField()

class Especialista(models.Model):
    nomUsuario = models.CharField(primary_key=True, max_length=8)
    nombre = models.CharField(max_length=70)
    contrasena = models.CharField(max_length=50)
    correo = models.EmailField()
    numPacientes = models.IntegerField()
    datos_generales = models.CharField(max_length=200)

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
    escolaridad = models.CharField(choices=ESCOLARIDAD)
    fechaNac = models.DateField
    sexo = models.CharField(choices=GENDER)
    fechaIng = models.DateField
    fechaDiag = models.DateField


class Administrador(models.Model):
    nomUsuario = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=70)
    contrasena = models.CharField(max_length=45)
    correo = models.EmailField()

class Pregunta(models.Model):
    TIPO = [
        ('TXT', 'Texto'),
        ('IMG', 'Imagen'),
        ('AUD', 'Audio'),
    ]
    idReactivo = models.IntegerField(primary_key=True)
    pregunta = models.TextField()
    tipo = models.CharField(choices=TIPO)
    preguntaBin = models.BooleanField()

class Ap_Reminiscencia(models.Model):
    cveAcceso = models.CharField(primary_key=True, max_length=10)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField()

class Reminiscencia(models.Model):
    cveAcceso = models.ForeignKey(Ap_Reminiscencia, on_delete=models.CASCADE)
    idReactivo = models.ForeignKey(Pregunta, on_delete=models.CASCADE )
    respuestaPaciente = models.CharField(255)
    respuestaCuidador = models.CharField(255)
    resultado = models.IntegerField()
    unique_together = (('CveAcceso', ' idReactivo'))

class Ap_Screening(models.Model):
    cveAcceso = models.CharField(primary_key=True, max_length=10)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField()
    resultadoFinal = models.IntegerField()

class Screening(models.Model):
    idReactivo = models.IntegerField()
    cveAcceso = models.ForeignKey( Ap_Reminiscencia, on_delete=models.CASCADE)
    respuestaT = models.CharField(100)
    respuestaImg = models.ImageField()
    

class Tema(models.Model):
    DIFICULTAD=[
        ('F',"Facil"),
        ('M', "Medio"),
        ('D', "Dificil"),
    ]
    cveTemas = models.IntegerField(primary_key=True)
    tema = models.CharField(max_length=20)
    dificultad = models.CharField(choices=DIFICULTAD)

class Ent_Cogn(models.Model):
    STATUS = [
        ('S',"Superado"),
        ('NS',"No superado")
    ]
    cveAcceso = models.CharField(max_length=10, primary_key=True)
    cveTema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fechaAp = models.DateField
    estado =  models.CharField(choices=STATUS)
    tiempo = models.TimeField

class Mensaje(models.Model):
    cveMensaje = models.IntegerField(primary_key=True)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=200)
    fechaEnvio = models.DateField
    
class Palabra(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    cvePalabra = models.IntegerField(primary_key=True)
    palabra = models.CharField(max_length=10)