# Generated by Django 5.0.6 on 2024-05-24 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solucionario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocorrencia',
            name='autor',
            field=models.CharField(max_length=255, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='desc_ocorrencia',
            field=models.TextField(verbose_name='Descrição da Ocorrência'),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='desc_solução',
            field=models.TextField(verbose_name='Descrição da Solução'),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='print_ocorrencia',
            field=models.FileField(upload_to='media/', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='ocorrencia',
            name='titulo',
            field=models.CharField(max_length=255, verbose_name='Título'),
        ),
    ]