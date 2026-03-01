# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para algumas bibliotecas do Agno
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala manualmente o apscheduler caso não esteja no requirements
RUN pip install --no-cache-dir apscheduler

# Copia o restante do código do projeto
COPY . .

# Expõe a porta que o playground usa
EXPOSE 7777

# Comando para rodar a aplicação
CMD ["python", "playground.py"]
