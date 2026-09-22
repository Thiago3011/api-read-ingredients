# Usa uma imagem leve do Python
FROM python:3.12-slim

# Instala dependências do sistema, incluindo Tesseract e idioma português
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-por \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências primeiro
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Inicia a API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]