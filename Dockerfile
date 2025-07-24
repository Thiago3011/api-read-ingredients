# Usa imagem leve do Python
FROM python:3.10-slim

# Instala dependências do sistema, incluindo Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para dentro do contêiner
COPY . /app

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000 (usada pelo Flask)
EXPOSE 5000

# Comando que inicia a aplicação
CMD ["python", "app.py"]
