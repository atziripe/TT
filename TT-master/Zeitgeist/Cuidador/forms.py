from django import forms
from Pruebas.forms import dar_estilo_campos 

class FormEditarC(forms.Form):
    nvo_nombre = forms.CharField(label='Nuevo nombre (completo):', required=True) 
    nvo_nombreUsuario = forms.CharField(label='Nuevo nombre de usuario:', required=True) 
    nvo_correo = forms.CharField(label='Nuevo correo electrónico:', required=True)  
    nvo_contrasena = forms.CharField(label='Nueva contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Contraseña actual:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class IngresoDatosT(forms.Form):
   respuesta = forms.CharField(required=True)


class FormDatosImg(forms.Form):
    respuesta = forms.CharField(required=True)
    imagen = forms.ImageField(required=True)