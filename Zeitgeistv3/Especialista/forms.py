#Creando clases con API Forms de Django para generar formularios validados
from django import forms
from Paciente.forms import dar_estilo_campos 

class FormEditarE(forms.Form):
    nvo_nombre = forms.CharField(label='Nombre:', required=True) 
    nvo_apellidos = forms.CharField(label='Apellidos:', required=True)
    nvo_nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    nvo_correo = forms.EmailField(label='Correo Electrónico:', required=True) 
    nvos_datos_generales = forms.CharField(label='Datos generales:', required=True, widget=forms.Textarea)
    nvo_numPacientes = forms.IntegerField(label='Número de pacientes:', required=True, max_value=30, min_value=1,initial=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)