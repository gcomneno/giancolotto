# Usa un'immagine di Python come base
FROM python:3.8-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia i file del progetto
COPY requirements.txt /app/requirements.txt

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt
