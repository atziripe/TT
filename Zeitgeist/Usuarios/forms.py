#Creando clases con API Forms de Django para generar formularios validados
from django import forms


TYPEU =( 
    ("1", "Administrador"), 
    ("2", "Cuidador"), 
    ("3", "Especialista"), 
    ("4", "Paciente"), 
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
    sexo = forms.CharField(label='Género:', required=True)
    fechaNac = forms.CharField(label='Fecha de Nacimiento:', required=True)
    escolaridad = forms.CharField(label='Escolaridad:', required=True)
    fechaDiag = forms.CharField(label='Fecha de Diagnóstico:', required=True)

'''class FormRegistroE(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario (cédula profesional de especialista):', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    datos_generales = forms.CharField(label='Datos generales (Unidad Médica, cédula profesional, datos de contacto):', required=True)
    numPacientes = forms.CharField(label='Número de pacientes:', required=True)


class FormRegistroA(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)

'''
