from rest_framework import serializers
from .models import Cuidador
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserSerializer(serializers.ModelSerializer):
    cuidadores = serializers.PrimaryKeyRelatedField(many=True, queryset=Cuidador.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'cuidadores']

class CuidadorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Cuidador
        fields = (
            'nomUsuario',
            'nombre',
            'contrasena',
            'correo',
            'owner',
        )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, cuidador):
        token = super().get_token(cuidador)

        # Add custom claims
        token['username'] = cuidador.nomUsuario
        token["name"] = cuidador.nombre
        token['email'] = cuidador.correo
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer