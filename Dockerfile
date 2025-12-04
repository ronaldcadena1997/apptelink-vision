# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias (incluye Expo CLI local)
RUN npm install --legacy-peer-deps

# Instalar dependencias faltantes que Metro necesita
RUN npm install is-arrayish --legacy-peer-deps || true

# Copiar código fuente
COPY . .

# Dar permisos de ejecución a binarios de node_modules
RUN chmod -R +x node_modules/.bin/ 2>/dev/null || true

# Construir aplicación web
RUN npm run build

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

