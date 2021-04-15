#Creando clases con API Forms de Django para generar formularios validados
from django import forms


TYPEU =( 
    ("1", "Administrador"), 
    ("2", "Cuidador"), 
    ("3", "Especialista"), 
    ("4", "Paciente"), 
)

Escolaridad_enum =(
    ('N','Ninguna'),
    ('PR','Primaria'),
    ('SC','Secundaria'),
    ('BCH','Bachillerato'),
    ('SUP','Licenciatura o superior'),
)

sexo_enum = (
    ('F', "Femenino"),
    ('M', "Masculino"),
)
  
class FormLogin(forms.Form):
    tipo = forms.ChoiceField(choices = TYPEU,label="Usted está ingresando como ", required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    username = forms.CharField(label='Nombre de usuario', required=True) 
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)

class FormRegistroC(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)

class FormRegistroP(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    sexo = forms.ChoiceField(choices = sexo_enum, label='Género:', required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    fechaNac = forms.CharField(label='Fecha de Nacimiento:', required=True)
    escolaridad = forms.ChoiceField(choices = Escolaridad_enum, label='Escolaridad:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))
    fechaDiag = forms.CharField(label='Fecha de Diagnóstico:', required=True)

'''class FormRegistroE(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario (cédula profesional de especialista):', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    datos_generales = forms.CharField(label='Datos generales (Unidad Médica, cédula profesional, datos de contacto):', required=True)
    numPacientes = forms.CharField(label='Número de pacientes:', required=True)
'''

class FormRegistroA(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)


class FormrecuperarPass(forms.Form):
    correo = forms.EmailField(label='Correo electrónico:', required=True)
    