from django.shortcuts import render
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import authentication_classes, permission_classes
from .models import Cuidador
from .serializers import CuidadorSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions


def inicioC(request):
    return render(request, "Cuidador/inicioCuidador.html")

def editC(request):
    return render(request, "Cuidador/editarCuidador.html")

def ingrDatosC (request):
    return render(request, "Cuidador/IngresarDatosCuidador.html")


class CuidadorList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CuidadorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer