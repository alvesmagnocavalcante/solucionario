from django.db import models
import datetime

class Ocorrencia(models.Model):
    
    titulo = models.CharField(max_length=255, verbose_name='Título')
    desc_ocorrencia = models.TextField(verbose_name='Descrição da Ocorrência')
    desc_solução = models.TextField(verbose_name='Descrição da Solução')
    print_ocorrencia = models.FileField(upload_to='media/', verbose_name='Imagem', blank=True, null=True)
    autor = models.CharField(max_length=255, verbose_name='Autor')
    data = models.DateField(default=datetime.date.today, verbose_name='Data')
    
    def __str__(self):
        return self.titulo