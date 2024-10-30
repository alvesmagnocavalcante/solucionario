from django.contrib import admin
from .models import Ocorrencia


@admin.register(Ocorrencia)
class SolucionarioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 
                    'desc_ocorrencia', 
                    'desc_solução', 
                    'print_ocorrencia', 
                    'autor']
    
    search_fields = ['titulo', 
                    'desc_ocorrencia', 
                    'desc_solução', 
                    'print_ocorrencia', 
                    'autor']