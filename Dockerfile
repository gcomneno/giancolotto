# Usa un'immagine di Python come base
FROM python:3.8-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia i file sorgente nella directory di lavoro del container
COPY ./src /app/src
COPY ./config.ini /app/config.ini

# Copia i file del progetto
COPY requirements.txt /app/requirements.txt

# Installa le dipendenze
RUN pip install --no-cache-dir --progress-bar off --upgrade pip
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# Comando di avvio dell'applicazione
# CMD [ "python", "./src/main.py" ]
