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


class UpdatePacientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ('sexo', 'escolaridad', 'fechaDiag')

    def update(self, instance, validated_data):
        instance.sexo = validated_data['sexo']
        instance.escolaridad = validated_data['escolaridad']
        instance.fechaDiag = validated_data['fechaDiag']
        instance.save()

        return instance

class UpdateEspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = ('datos_generales', 'numPacientes')

    def update(self, instance, validated_data):
        instance.datos_generales= validated_data['datos_generales']
        instance.numPacientes= validated_data['numPacientes']
        instance.save()

        return instance


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


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_username(self, value):
        user = self.context['request'].user
        print(user)
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "El usuario que escogiste ya existe o es el mismo al que tenías anteriormente."})
        return value

    def update(self, instance, validated_data):
        # user = self.context['request'].user

        # if user.pk != instance.pk:
        #     raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.email = validated_data['email']

        instance.save()

        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
