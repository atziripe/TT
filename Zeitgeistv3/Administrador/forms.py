#Creando clases con API Forms de Django para generar formularios validados
from django import forms
from Paciente.forms import dar_estilo_campos 


class FormEditarA(forms.Form):
    nvo_nombre = forms.CharField(label='Nombre:', required=True, widget=forms.Textarea)
    nvo_apellidos = forms.CharField(label='Apellidos:', required=True)
    nvo_nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True)
    nvo_correo = forms.EmailField(label='Correo Electrónico:', required=True) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormModificarRelacion(forms.Form):
    paciente = forms.CharField(label='Paciente a modificar:', required=True, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
        
'''class FormEliminarPerfil(forms.Form):
    perfil = forms.CharField(label='Usuario a eliminar:', required=True, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)'''