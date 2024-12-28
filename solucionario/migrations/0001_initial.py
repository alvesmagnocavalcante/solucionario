# Generated by Django 5.0.6 on 2024-05-24 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ocorrencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('desc_ocorrencia', models.TextField()),
                ('desc_solução', models.TextField()),
                ('print_ocorrencia', models.FileField(upload_to='media/')),
                ('autor', models.CharField(max_length=255)),
            ],
        ),
    ]