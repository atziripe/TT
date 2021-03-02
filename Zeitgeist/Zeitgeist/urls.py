"""Zeitgeist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Zeitgeist.views import inicioPa, inicioC, inicio, rmsc1, rmsc2, rmsc3, editC, editP, regC, regP, recPasswd, ingrDatosC

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', inicio), 
    path('inicioP/', inicioPa), 
    path('inicioC/', inicioC),
    path('reminiscencia-1/', rmsc1),
    path('reminiscencia-2/', rmsc2),
    path('reminiscencia-3/', rmsc3),
    path('editarC/', editC),
    path('editarP/', editP),
    path('registroC/', regC),
    path('registroP/', regP),
    path('recuperarPass/', recPasswd),
    path('ingresarDatosC/', ingrDatosC),
]
