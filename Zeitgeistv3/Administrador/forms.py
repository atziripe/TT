#Creando clases con API Forms de Django para generar formularios validados
from django import forms
from django.contrib.auth.models import User, Group
from Paciente.forms import dar_estilo_campos 

def obtenerLista(listaU):
	listaFinal = [('Ninguno', 'Ninguno'),]

	for usuario in listaU:
		par_lista = []
		par_lista.append(usuario['id'])
		par_lista.append(usuario['username'])
		tupla = tuple(par_lista)
		listaFinal.append(tupla)

	tuplaFinal = tuple(listaFinal)
	return tuplaFinal


def ListaCuidadores():
	cuidadores = list(Group.objects.get(name="Cuidadores").user_set.all().values())
	return obtenerLista(cuidadores)

def ListaEspecialistas():
	especialistas = list(Group.objects.get(name="Especialistas").user_set.all().values())
	return obtenerLista(especialistas)


class FormEditarA(forms.Form):
    nvo_nombre = forms.CharField(label='Nombre:', required=True, widget=forms.Textarea)
    nvo_apellidos = forms.CharField(label='Apellidos:', required=True)
    nvo_nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True)
    nvo_correo = forms.EmailField(label='Correo Electrónico:', required=True) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormEditarRelacionesP(forms.Form):
    nvo_cuidador = forms.ChoiceField(choices = ListaCuidadores(), label='Cuidador:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))
    nvo_especialista = forms.ChoiceField(choices = ListaEspecialistas(), label='Especialista:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

