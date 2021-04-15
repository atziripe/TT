from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Usuarios.urls')),
    path('paciente/', include('Pruebas.urls'),name='inicioP'),
    path('cuidador/', include('Cuidador.urls'),name='inicioC'),
<<<<<<< HEAD
    path('especialista/', include('Especialista.urls'), name='InicioE'),
=======
    path('especialista/', include('Especialista.urls'),name='inicioE'),
    path('administrador/', include('Administrador.urls'), name='inicioA'),
>>>>>>> 1f8d1b344bf99061a0bdae79ab6b28bc118e9111
    path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
