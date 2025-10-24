# Dockerfile para deployment opcional en Docker
FROM python:3.11-slim

# Instalar FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY *.md ./

# Configurar puerto para health check
ENV PORT=8080

# Comando para iniciar el bot
CMD ["python", "-m", "src.bot"]
