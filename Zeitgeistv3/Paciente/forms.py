from django import forms
from Usuario.forms import dateInput

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

def dar_estilo_campos(listaCampos): #Brinda el formato apropiado a los campos del formulario
    campos = ['nvo_nombre', 'nvo_nombreUsuario', 'nvo_correo', 'nvo_contrasena', 'confirmacion_cont', 'nvos_datos_generales', 'nvo_numPacientes', 'nvo_fechaNac', 'nvo_fechaDiag', 'paciente', 'perfil']
    for campo in campos:
        try:
        #Asignamos los valores a los campos que si existen en los formularios...
            listaCampos[campo].widget.attrs.update({'class': 'black-text', "style": "font-size: 18px;"})
            listaCampos[campo].widget.attrs['style']  = 'width:100%; height: 30px; background-color: #fff;'
        except: #Si no existe, ejecutamos una excepción y nos pasamos al siguiente campo de "campos"
            campo = 'Inexistente'


class FormEditarP(forms.Form):
    nvo_nombre = forms.CharField(label='Nombre:', required=True) 
    nvo_apellidos = forms.CharField(label='Apellidos:', required=True) 
    nvo_nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    nvo_sexo = forms.ChoiceField(choices = sexo_enum, label='Género:', required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    nvo_escolaridad = forms.ChoiceField(choices = Escolaridad_enum, label='Nivel de escolaridad:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))
    nvo_fechaDiag = forms.CharField(label='Fecha de Diagnóstico:', required=True,  widget=dateInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)