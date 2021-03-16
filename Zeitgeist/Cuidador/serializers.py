from rest_framework import serializers
from .models import Cuidador
from django.contrib.auth.models import User

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