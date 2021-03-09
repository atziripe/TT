from django.db import models
from Usuarios.models import Usuario

# Create your models here.
class Cuidador(models.Model):
    nomUsuario = models.ForeignKey(Usuario, on_delete= models.CASCADE, primary_key=True)
