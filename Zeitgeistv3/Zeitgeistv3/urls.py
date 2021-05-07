from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Usuario.urls')),
    path('paciente/', include('Paciente.urls'),name='inicioP'),
    path('cuidador/', include('Cuidador.urls'),name='inicioC'),
    path('especialista/', include('Especialista.urls'), name='InicioE'),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

