from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, View
import io
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from .models import Ocorrencia
from .forms import OcorrenciaForm
from reportlab.lib.utils import ImageReader
from django.db.models import Q
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image  # Adicionando as importações necessárias

# View para listar as ocorrências
class ListaOcorrenciaView(ListView):
    model = Ocorrencia
    template_name = 'lista_ocorrencia.html'
    context_object_name = 'lista_ocorrencia'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(titulo__icontains=search_query)  # Filtro insensível a maiúsculas/minúsculas
        return queryset

# View para criar uma nova ocorrência
class CriaOcorrenciaView(CreateView):
    model = Ocorrencia
    template_name = 'cria_ocorrencia.html'
    form_class = OcorrenciaForm
    success_url = reverse_lazy('lista_ocorrencia')

# View para detalhes de uma ocorrência
class DetalhesOcorrenciaView(DetailView):
    model = Ocorrencia
    template_name = 'detalhes_ocorrencia.html'
    context_object_name = 'ocorrencia'

# View para download do PDF da ocorrência
class DownloadOcorrenciaPDF(View):
    def get(self, request, pk):
        ocorrencia = Ocorrencia.objects.get(pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ocorrencia_{ocorrencia.id}.pdf"'

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        styles = getSampleStyleSheet()
        story.append(Paragraph(f"Título: {ocorrencia.titulo}", styles['Title']))
        story.append(Paragraph(f"Descrição da Ocorrência: {ocorrencia.desc_ocorrencia}", styles['BodyText']))
        story.append(Paragraph(f"Descrição da Solução: {ocorrencia.desc_solução}", styles['BodyText']))
        story.append(Paragraph(f"Autor: {ocorrencia.autor}", styles['BodyText']))

        # Corrigindo o formato da data para DD/MM/AAAA
        data_formatada = ocorrencia.data.strftime("%d/%m/%Y")
        story.append(Paragraph(f"Data: {data_formatada}", styles['BodyText']))

        # Adicionando a imagem com proporções corretas
        if ocorrencia.print_ocorrencia:
            image_path = ocorrencia.print_ocorrencia.path
            image_reader = ImageReader(image_path)
            img_width, img_height = image_reader.getSize()

            # Definindo o novo tamanho da imagem mantendo a proporção
            max_width, max_height = 200, 200
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = img_width * ratio
            new_height = img_height * ratio

            image = Image(image_path, width=new_width, height=new_height)
            story.append(image)

        doc.build(story)

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
