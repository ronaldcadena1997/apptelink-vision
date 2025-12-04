# Usar Python 3.11 como base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de archivos
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando para iniciar
CMD ["python", "server.py"]

