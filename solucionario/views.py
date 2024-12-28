from django.http import HttpResponse, Http404
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image  # Adicionando imports necessários
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io
from .models import Ocorrencia
from .forms import OcorrenciaForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, View

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
        try:
            ocorrencia = Ocorrencia.objects.get(pk=pk)  # Tentando buscar a Ocorrência pelo pk
        except Ocorrencia.DoesNotExist:
            raise Http404("Ocorrência não encontrada.")  # Caso não encontre, levanta um erro 404

        # Configurando a resposta como um PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ocorrencia_{ocorrencia.id}.pdf"'

        # Criando o documento PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Definindo estilos para o texto do PDF
        styles = getSampleStyleSheet()
        story.append(Paragraph(f"Título: {ocorrencia.titulo}", styles['Title']))
        story.append(Paragraph(f"Descrição da Ocorrência: {ocorrencia.desc_ocorrencia}", styles['BodyText']))
        story.append(Paragraph(f"Descrição da Solução: {ocorrencia.desc_solução}", styles['BodyText']))
        story.append(Paragraph(f"Autor: {ocorrencia.autor}", styles['BodyText']))

        # Formatando a data no formato DD/MM/YYYY
        data_formatada = ocorrencia.data.strftime("%d/%m/%Y")
        story.append(Paragraph(f"Data: {data_formatada}", styles['BodyText']))

        # Adicionando a imagem se existir e ajustando seu tamanho
        if ocorrencia.print_ocorrencia:
            image_path = ocorrencia.print_ocorrencia.path
            image_reader = ImageReader(image_path)
            img_width, img_height = image_reader.getSize()

            # Ajustando o tamanho da imagem para que ela caiba em um espaço de 200x200
            max_width, max_height = 200, 200
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = img_width * ratio
            new_height = img_height * ratio

            image = Image(image_path, width=new_width, height=new_height)
            story.append(image)

        # Gerando o PDF
        doc.build(story)

        # Enviando o conteúdo do PDF para a resposta HTTP
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
