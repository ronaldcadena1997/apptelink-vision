# Dockerfile para Arquitectura Estilo Hikvision
# Este Dockerfile está en la raíz para que Railway lo encuentre fácilmente

FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN pip install --upgrade pip

# Copiar requirements desde backend
COPY backend/requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos necesarios del backend
COPY backend/server_hikvision_style.py .
COPY backend/config.py .

# Verificar que los archivos existen
RUN ls -la /app/server_hikvision_style.py && \
    ls -la /app/config.py && \
    echo "✅ Archivos copiados correctamente"

# Exponer puerto (Railway usa PORT automáticamente)
EXPOSE 8080

# Comando para iniciar el servidor estilo Hikvision
CMD ["python", "server_hikvision_style.py"]
