# Usar Node 18
FROM node:18-alpine

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar todo el código
COPY . .

# Exponer puerto
EXPOSE 8081

# Variable de entorno para producción
ENV NODE_ENV=production

# Iniciar servidor web de Expo
CMD ["npx", "expo", "start", "--web", "--port", "8081"]

