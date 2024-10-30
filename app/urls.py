from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from solucionario.views import ListaOcorrenciaView, CriaOcorrenciaView, DetalhesOcorrenciaView, DownloadOcorrenciaPDF

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detalhes/<int:pk>/download/', DownloadOcorrenciaPDF.as_view(), name='download_ocorrencia_pdf'),
    path('', ListaOcorrenciaView.as_view(), name='lista_ocorrencia'),
    path('ocorrencias/criar/', CriaOcorrenciaView.as_view(), name='cria_ocorrencia'),
    path('ocorrencias/<int:pk>/', DetalhesOcorrenciaView.as_view(), name='detalhes_ocorrencia'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
