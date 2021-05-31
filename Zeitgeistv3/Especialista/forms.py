#Creando clases con API Forms de Django para generar formularios validados
from django import forms

def dar_estilo_campos(listaCampos): #Brinda el formato apropiado a los campos del formulario
    campos = ['nvo_nombre', 'nvo_apellidos', 'nvo_correo', 'nvos_datos_generales', 'nvo_numPacientes', 'cuidador']
    for campo in campos:
        try:
        #Asignamos los valores a los campos que si existen en los formularios...
            listaCampos[campo].widget.attrs.update({'class': 'black-text', "style": "font-size: 18px;"})
            listaCampos[campo].widget.attrs['style']  = 'width:100%; height: 30px; background-color: #fff;'
        except: #Si no existe, ejecutamos una excepción y nos pasamos al siguiente campo de "campos"
            campo = 'Inexistente'

class FormEditarE(forms.Form):
    nvo_nombre = forms.CharField(label='Nombre:', required=True) 
    nvo_apellidos = forms.CharField(label='Apellidos:', required=True)
    nvo_correo = forms.EmailField(label='Correo Electrónico:', required=True) 
    nvos_datos_generales = forms.CharField(label='Datos generales:', required=True, widget=forms.Textarea)
    nvo_numPacientes = forms.IntegerField(label='Cantidad de pacientes nuevos por atender:', required=True, max_value=30, min_value=0,initial=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)


class FormMensaje(forms.Form):
	cuidador = forms.CharField(label="Cuidador:", required=True, widget=forms.TextInput(attrs={'readonly':'readonly', 'style': 'text-align:center; width:100%; height: 30px; background-color: #fff; font-size: 18px;', 'class': 'black-text'}))
	mensaje = forms.CharField(label='Mensaje:', required=True, widget=forms.Textarea(attrs={'placeholder':'Escriba el mensaje aquí', 'style': 'width:100%; height: 150px; background-color: #fff; font-size: 17px;', 'class': 'black-text'}))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)