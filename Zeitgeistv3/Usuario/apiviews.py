from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Paciente, Especialista, Cuidador, Administrador
from .serializers import PacienteSerializer, AdministradorSerializer, EspecialistaSerializer, CuidadorSerializer, UserSerializer, MyTokenObtainPairSerializer, ChangePasswordSerializer, UpdateUserSerializer, UpdatePacientSerializer, UpdateEspecialistaSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# *******************Registro de usuarios sin necesidad de auth******************************


#Se crea el registro en los 4 tipos de usuario
class PacienteCreate(generics.CreateAPIView):
    serializer_class = PacienteSerializer


class EspecialistCreate(generics.CreateAPIView):
    serializer_class = EspecialistaSerializer


class CuidadorCreate(generics.CreateAPIView):
    serializer_class = CuidadorSerializer


class AdminCreate(generics.CreateAPIView):
    serializer_class = AdministradorSerializer
    #permission_classes = [IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

# *******************List***********************

class ListPaciente(generics.ListAPIView):  # Para especialistas y administradores
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]


class ListEspecialista(generics.ListAPIView):  # Para administradores
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer
    permission_classes = [IsAuthenticated]


class ListCuidador(generics.ListAPIView):  # Para administradores
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer
    permission_classes = [IsAuthenticated]


class ListAdministrador(generics.ListAPIView):  # Para administradores
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]


class ListUsers(generics.ListAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]

# *******************consulta por user***********************

class PacienteUser(APIView):
    def get(self, request, pk):
        payload = get_object_or_404(Paciente, user=pk)
        data = PacienteSerializer(payload).data
        return Response(data)

class EspecialistaUser(APIView):
    def get(self, request, pk):
        payload = get_object_or_404(Especialista, user=pk)
        data = EspecialistaSerializer(payload).data
        return Response(data)

class CuidadorUser(APIView):
    def get(self, request, pk):
        payload = get_object_or_404(Cuidador, user=pk)
        data = CuidadorSerializer(payload).data
        return Response(data)

class AdministradorUser(APIView):
    def get(self, request, pk):
        payload = get_object_or_404(Administrador, user=pk)
        data = AdministradorSerializer(payload).data
        return Response(data)


# *******************Retrieve Destroy Update***********************

class PacienteSelDel(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    #permission_classes = [IsAuthenticated]

class UpdatePacientView(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    #permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePacientSerializer

class EspecialistaSelDel(generics.RetrieveUpdateDestroyAPIView):
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer
    permission_classes = [IsAuthenticated]

class UpdateEspecialistaView(generics.UpdateAPIView):
    queryset = Especialista.objects.all()
    #permission_classes = (IsAuthenticated,)
    serializer_class = UpdateEspecialistaSerializer


class CuidadorSelDel(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cuidador.objects.all()
    serializer_class = CuidadorSerializer
    permission_classes = [IsAuthenticated]

class UserSelDel(generics.RetrieveUpdateDestroyAPIView): #Solo para admins
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]


# *******************Login***********************

class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

# *******************Change Password***********************


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer