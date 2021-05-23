#Creando clases con API Forms de Django para generar formularios validados
from django import forms
from django.contrib.auth.models import User, Group
from Usuario.models import Cuidador, Especialista
from Paciente.forms import dar_estilo_campos 

def obtenerLista(listaU):
	listaFinal = [('Ninguno', 'Ninguno'),]	
	lista_ids = []

	for usuario in listaU: 
		par_lista = []
		id_user = usuario['id']

		if (Cuidador.objects.filter(user_id=id_user)):
			info_user = list(Cuidador.objects.filter(user_id=id_user).values())
			par_lista.append(usuario['username']) 
		else:
			info_user = list(Especialista.objects.filter(user_id=id_user).values())
			par_lista.append(usuario['first_name']+' ' + usuario['last_name']) 

		for user in info_user: #Tenemos que sacar la ID de cuidador/doctor, no la de usuario
			id_user = user['id']
			par_lista.insert(0,id_user) #Una vez que la tenemos, añadimos a lo que sera la tupla
		
		tupla = tuple(par_lista) #Iremos haciendo tuplas (idGrupo, username)
		listaFinal.append(tupla)

	tuplaFinal = tuple(listaFinal) #En este punto ya tenemos una tupla por cada Usuario
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
    nvo_cuidador = forms.ChoiceField(label='Cuidador:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))
    nvo_especialista = forms.ChoiceField(label='Especialista:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	dar_estilo_campos(self.fields)
    	self.fields['nvo_cuidador'].choices = ListaCuidadores()
    	self.fields['nvo_especialista'].choices = ListaEspecialistas()
