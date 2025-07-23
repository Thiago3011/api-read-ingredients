# Usa uma imagem leve do Python
FROM python:3.11-slim

# Instala dependências do sistema e o Tesseract
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto para o container
COPY . /app
WORKDIR /app

# Expõe a porta 5000 (Flask)
EXPOSE 5000

# Comando para iniciar o app
CMD ["python", "app.py"]
