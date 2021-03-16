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
    highlighted = models.TextField(null = True)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.nomUsuario)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Cuidador, self).save(*args, **kwargs)