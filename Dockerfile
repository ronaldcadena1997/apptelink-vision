# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias globales y del proyecto
RUN npm install -g @expo/cli && \
    npm install

# Copiar código fuente
COPY . .

# Dar permisos a node_modules/.bin
RUN chmod -R +x node_modules/.bin || true

# Build de la aplicación web usando el script de package.json
RUN npm run build

# Stage 2: Servidor
FROM node:18-alpine

WORKDIR /app

# Instalar serve para servir archivos estáticos
RUN npm install -g serve

# Copiar build del stage anterior
COPY --from=builder /app/dist ./dist

# Exponer puerto
EXPOSE 3000

# Comando para servir la app
CMD ["serve", "dist", "-s", "-l", "3000"]

