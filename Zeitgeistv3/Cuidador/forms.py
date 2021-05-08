from django import forms
from Paciente.forms import dar_estilo_campos 

class FormEditarC(forms.Form):
    nvo_nombre = forms.CharField(label='Nombre:', required=True) 
    nvo_apellidos = forms.CharField(label='Apellidos:', required=True)
    nvo_nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    nvo_correo = forms.CharField(label='Correo Electrónico:', required=True)  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class IngresoDatosT(forms.Form):
   respuesta = forms.CharField(required=True)


class FormDatosImg(forms.Form):
    respuesta = forms.CharField(required=True)
    imagen = forms.ImageField(required=True)