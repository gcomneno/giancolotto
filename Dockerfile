# Usa un'immagine di Python come base
FROM python:3.8-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia l'intero progetto nel container
COPY . /app

# Installa le dipendenze
RUN pip install --no-cache-dir --progress-bar off --upgrade pip
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
RUN pip install colorama
