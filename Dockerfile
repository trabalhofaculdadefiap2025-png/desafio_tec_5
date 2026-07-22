# Usa uma imagem oficial e leve do Python 3.11
FROM python:3.11-slim

# Instala dependências de sistema necessárias para processamento de imagem (PIL / OpenCV)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt-get/lists/*

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . .

# Expõe a porta padrão utilizada pelo Streamlit
EXPOSE 8501

# Variável de ambiente para garantir que os logs do Python saiam em tempo real
ENV PYTHONUNBUFFERED=1

# Comando para iniciar o Streamlit binding no IP público do container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]