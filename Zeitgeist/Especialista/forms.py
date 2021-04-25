#Creando clases con API Forms de Django para generar formularios validados
from django import forms
from Pruebas.forms import dar_estilo_campos 

class FormEditarE(forms.Form):
    nvo_nombre = forms.CharField(label='Nuevo nombre (completo):', required=True) 
    nvo_nombreUsuario = forms.CharField(label='Nuevo nombre de usuario:', required=True) 
    nvo_correo = forms.CharField(label='Nuevo correo electrónico:', required=True)  
    nvo_contrasena = forms.CharField(label='Nueva contraseña:', required=True, widget=forms.PasswordInput)
    nvos_datos_generales = forms.CharField(label='Nuevos datos generales:', required=True, widget=forms.Textarea)
    nvo_numPacientes = forms.IntegerField(label='Nuevo número de pacientes:', required=True, max_value=30, min_value=1,initial=1)
    confirmacion_cont = forms.CharField(label='Contraseña actual:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)