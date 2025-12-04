# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Instalar Expo CLI globalmente
RUN npm install -g @expo/cli

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Dar permisos de ejecución
RUN chmod +x node_modules/.bin/* || true

# Construir aplicación web usando Expo CLI directamente
RUN npx --yes @expo/cli export --platform web

# Stage 2: Servidor
FROM node:18-alpine

WORKDIR /app

# Instalar serve
RUN npm install -g serve

# Copiar build
COPY --from=builder /app/dist ./dist

# Exponer puerto (Railway usa variable PORT)
EXPOSE 3000

# Servir archivos estáticos
CMD serve dist -s -p ${PORT:-3000}

