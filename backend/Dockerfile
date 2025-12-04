# Usar Python 3.11 como base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar solo dependencias mínimas del sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de archivos
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando para iniciar
CMD ["python", "server.py"]

