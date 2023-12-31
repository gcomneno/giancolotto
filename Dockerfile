# Usa un'immagine di Python come base
FROM python:3.8

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia i file di configurazione
COPY config.ini /app/config.ini

# Copia i file del progetto
COPY lotto_extractor.py /app/lotto_extractor.py
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Comando di avvio dell'applicazione
#CMD ["python", "main.py"]
