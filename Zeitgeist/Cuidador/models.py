from django.db import models
from django_cryptography.fields import encrypt
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight 


# Create your models here.
class Cuidador(models.Model):
    nomUsuario = models.CharField(primary_key = True, max_length=20)
    nombre = models.CharField(max_length=70)
    contrasena = models.CharField(max_length=45)
    correo = models.EmailField()
    owner = models.ForeignKey('auth.User', related_name='cuidadores', on_delete=models.CASCADE, null=True)
    #highlighted = models.TextField(null = True)
    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name('python')
    #     linenos = 'table' if True else False
    #     options = {'title': self.nombre} if self.nombre else {}
    #     formatter = HtmlFormatter(style='monokai', linenos=linenos,
    #                             full=True, **options)
    #     self.highlighted = highlight(args, lexer, formatter)
    #     super(Cuidador, self).save(*args, **kwargs)

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

