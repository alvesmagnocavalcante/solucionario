FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Crie um script de entrada
RUN echo '#!/bin/bash\n\
python manage.py makemigrations\n\
python manage.py migrate\n\
exec python manage.py runserver 0.0.0.0:8000' > start.sh \
    && chmod +x start.sh

# Execute o script de inicialização
CMD ["./start.sh"]
