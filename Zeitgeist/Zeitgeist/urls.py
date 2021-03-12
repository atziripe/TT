from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Usuarios.urls')),
    path('paciente/', include('Pruebas.urls'),name='inicioP'),
    path('cuidador/', include('Cuidador.urls'),name='inicioC'),
    path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
]
