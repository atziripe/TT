from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Paciente, Especialista, Cuidador, Administrador
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        print(token)
        return token


class CuidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model =Cuidador
        fields='__all__'

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Especialista
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Paciente
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer): #Serializador de usuarios (en este ejemplo usamos los users de Django pero si queremos sobreescribir la clase Usuario, se hace el modelo en models.py)
    class Meta:
        model = User
        fields = ('id','username','email','password', 'first_name', 'last_name', 'groups')
        extra_kwargs = {'password':{'write_only':True}} #no regresa la contraseña en el response, por eso solo se escribe
    
    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])#Cifrar password
        user.save()
        return user

