# 📹 AppTelink Vision

Sistema de vigilancia inteligente con detección de intrusos para cámaras IP.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Android%20%7C%20iOS%20%7C%20Web-green.svg)
![License](https://img.shields.io/badge/license-Private-red.svg)

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Ejecutar la API (Backend)](#-ejecutar-la-api-backend)
- [Ejecutar la Aplicación Web](#-ejecutar-la-aplicación-web)
- [Ejecutar en Android (QR Code)](#-ejecutar-en-android-qr-code)
- [Ejecutar en iOS (QR Code)](#-ejecutar-en-ios-qr-code)
- [Credenciales de Acceso](#-credenciales-de-acceso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Endpoints de la API](#-endpoints-de-la-api)

---

## 🔧 Requisitos Previos

### Para el Frontend (React Native/Expo)

| Requisito | Versión | Descarga |
|-----------|---------|----------|
| Node.js | 18+ (LTS) | [nodejs.org](https://nodejs.org/) |
| npm | 9+ | Incluido con Node.js |

### Para el Backend (API Python)

| Requisito | Versión | Descarga |
|-----------|---------|----------|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| pip | Última | Incluido con Python |

### Para dispositivos móviles

| Plataforma | App requerida |
|------------|---------------|
| Android | [Expo Go](https://play.google.com/store/apps/details?id=host.exp.exponent) |
| iOS | [Expo Go](https://apps.apple.com/app/expo-go/id982107779) |

---

## 📥 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
```

### 2. Instalar dependencias del Frontend

```bash
npm install
```

### 3. Instalar dependencias del Backend

**Opción A: Usando el script automático**
```bash
cd backend
.\instalar_dependencias.bat
```

**Opción B: Instalación manual**
```bash
cd backend
pip install -r requirements.txt
```

Las dependencias del backend son:
- `flask==3.0.0` - Framework web
- `flask-cors==4.0.0` - Manejo de CORS
- `opencv-python==4.8.1.78` - Procesamiento de video/imágenes

---

## 🖥️ Ejecutar la API (Backend)

El servidor API es necesario para el funcionamiento de las cámaras y detección de intrusos.

### Opción A: Usando el script automático (Recomendado)

```bash
cd backend
.\iniciar_servidor.bat
```

### Opción B: Ejecución manual

```bash
cd backend
python server.py
```

### Verificar que el servidor está funcionando

Una vez iniciado, verás:

```
============================================================
       SERVIDOR API - APPTELINK VISION
============================================================

Iniciando servidor en http://0.0.0.0:5000

Endpoints disponibles:
  GET  /api/status              - Estado del servidor
  GET  /api/camaras/detectar    - Detectar cámaras
  GET  /api/camaras             - Listar cámaras
  GET  /api/camaras/<ip>/snapshot - Capturar imagen
  GET  /api/cercas              - Obtener cercas
  POST /api/cercas              - Guardar cercas
  GET  /api/intrusos            - Listar imágenes
  GET  /api/intrusos/<archivo>  - Obtener imagen
============================================================

 * Running on http://127.0.0.1:5000
 * Running on http://192.168.60.15:5000
```

**URLs de acceso:**
- Local: `http://localhost:5000`
- Red local: `http://192.168.60.15:5000` (puede variar según tu IP)

---

## 🌐 Ejecutar la Aplicación Web

### Paso 1: Asegúrate de que la API esté ejecutándose

Ver sección anterior [Ejecutar la API](#-ejecutar-la-api-backend)

### Paso 2: Iniciar el servidor web

```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
npm run web
```

### Paso 3: Acceder a la aplicación

Una vez iniciado, la aplicación estará disponible en:

```
🌐 http://localhost:8081
```

El navegador debería abrirse automáticamente. Si no, copia la URL y pégala manualmente.

---

## 📱 Ejecutar en Android (QR Code)

### Requisitos

1. ✅ Tener instalada la app **Expo Go** desde [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
2. ✅ El teléfono y la computadora deben estar en la **misma red WiFi**
3. ✅ La API debe estar ejecutándose

### Pasos

1. **Iniciar el servidor Expo:**

```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
npx expo start
```

2. **Escanear el código QR:**
   - Se mostrará un código QR en la terminal
   - Abre la app **Expo Go** en tu Android
   - Toca en "Scan QR code"
   - Escanea el código QR mostrado en la terminal

3. **Alternativa: Ingreso manual de URL**
   - En Expo Go, toca "Enter URL manually"
   - Ingresa: `exp://192.168.60.100:8081` (la IP puede variar)

### Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `a` | Abrir en emulador Android (si está instalado) |
| `r` | Recargar la aplicación |
| `m` | Abrir menú de desarrollo |
| `j` | Abrir debugger |

---

## 🍎 Ejecutar en iOS (QR Code)

### Requisitos

1. ✅ Tener instalada la app **Expo Go** desde [App Store](https://apps.apple.com/app/expo-go/id982107779)
2. ✅ El iPhone/iPad y la computadora deben estar en la **misma red WiFi**
3. ✅ La API debe estar ejecutándose

### Pasos

1. **Iniciar el servidor Expo:**

```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
npx expo start
```

2. **Escanear el código QR:**
   - Se mostrará un código QR en la terminal
   - Abre la app **Cámara** nativa de iOS
   - Apunta al código QR
   - Aparecerá una notificación "Abrir en Expo Go"
   - Toca la notificación para abrir la app

3. **Alternativa desde Expo Go:**
   - Abre la app Expo Go
   - Toca en "Scan QR code"
   - Escanea el código QR

### Atajos de teclado

| Tecla | Acción |
|-------|--------|
| `i` | Abrir en simulador iOS (solo en Mac) |
| `r` | Recargar la aplicación |
| `m` | Abrir menú de desarrollo |
| `j` | Abrir debugger |

---

## 🔐 Credenciales de Acceso

Para acceder a la aplicación (modo demo):

| Campo | Valor |
|-------|-------|
| **Usuario** | `admin` |
| **Contraseña** | `admin` |

---

## 📁 Estructura del Proyecto

```
proyectowebApptelinkVision/
├── 📄 App.js                    # Archivo principal con navegación
├── 📄 app.json                  # Configuración de Expo
├── 📄 package.json              # Dependencias del frontend
├── 📄 babel.config.js           # Configuración de Babel
├── 📄 README.md                 # Este archivo
├── 📄 INSTRUCCIONES.txt         # Instrucciones básicas
│
├── 📁 assets/                   # Recursos estáticos
│   ├── 🖼️ logo.png              # Logo de la empresa
│   ├── 🖼️ icon.png              # Icono de la app
│   ├── 🖼️ favicon.png           # Favicon para web
│   ├── 🖼️ adaptive-icon.png     # Icono adaptativo Android
│   └── 🖼️ splash-icon.png       # Imagen de splash screen
│
├── 📁 backend/                  # Servidor API Python
│   ├── 📄 server.py             # Servidor Flask
│   ├── 📄 requirements.txt      # Dependencias Python
│   ├── 📄 iniciar_servidor.bat  # Script para iniciar servidor
│   └── 📄 instalar_dependencias.bat # Script de instalación
│
├── 📁 src/                      # Código fuente
│   ├── 📁 config/
│   │   └── 📄 api.js            # Configuración de endpoints
│   │
│   └── 📁 screens/              # Pantallas de la app
│       ├── 📄 LoginScreen.js         # Inicio de sesión
│       ├── 📄 HomeScreen.js          # Menú principal
│       ├── 📄 CamaraScreen.js        # Vista de cámaras
│       ├── 📄 MonitoreoScreen.js     # Monitoreo en vivo
│       ├── 📄 ConfiguracionScreen.js # Configuración
│       ├── 📄 VideosScreen.js        # Reproductor de videos
│       └── 📄 IntrusosScreen.js      # Galería de intrusos
│
└── 📁 node_modules/             # Dependencias instaladas
```

---

## 🔌 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/status` | Estado del servidor |
| `GET` | `/api/camaras/detectar` | Detectar cámaras en la red |
| `GET` | `/api/camaras` | Listar cámaras configuradas |
| `GET` | `/api/camaras/<ip>/snapshot` | Capturar imagen de cámara |
| `GET` | `/api/cercas` | Obtener cercas virtuales |
| `POST` | `/api/cercas` | Guardar cercas virtuales |
| `GET` | `/api/intrusos` | Listar imágenes de intrusos |
| `GET` | `/api/intrusos/<archivo>` | Obtener imagen específica |

### Ejemplo de uso

```bash
# Verificar estado del servidor
curl http://localhost:5000/api/status

# Detectar cámaras
curl http://localhost:5000/api/camaras/detectar

# Listar cámaras
curl http://localhost:5000/api/camaras
```

---

## 🚀 Comandos Rápidos

### Iniciar todo (Backend + Frontend Web)

**Terminal 1 - Backend:**
```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
.\iniciar_servidor.bat
```

**Terminal 2 - Frontend:**
```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
npm run web
```

### Iniciar para móviles (Backend + Expo)

**Terminal 1 - Backend:**
```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision\backend
.\iniciar_servidor.bat
```

**Terminal 2 - Expo:**
```bash
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
npx expo start
```

---

## ⚠️ Solución de Problemas

### El servidor no inicia

1. Verificar que Python esté instalado: `python --version`
2. Verificar que las dependencias estén instaladas: `pip list`
3. Reinstalar dependencias: `pip install -r requirements.txt`

### No puedo escanear el QR

1. Verificar que el teléfono y PC estén en la misma red WiFi
2. Desactivar temporalmente el firewall de Windows
3. Usar la opción de túnel: `npx expo start --tunnel`

### La app no carga en el navegador

1. Limpiar caché: `npx expo start --clear`
2. Verificar que el puerto 8081 esté libre
3. Reinstalar node_modules: `rm -rf node_modules && npm install`

### Error de conexión con la API

1. Verificar que el servidor Python esté ejecutándose
2. Verificar la IP correcta en `src/config/api.js`
3. Probar la API directamente: `http://localhost:5000/api/status`

---

## 🌍 Deployment / Hosting en Internet

¿Quieres acceder a tu aplicación desde cualquier lugar?

📄 **Lee la [Guía de Deployment](DEPLOYMENT.md)** para hostear tu aplicación en:
- Railway (Gratis)
- Render (Gratis)
- Vercel (Gratis para frontend)

**Tiempo estimado: 10 minutos** ⚡

---

## 🌐 **Backend en Servidor + NUC Local**

### **Arquitectura Recomendada:**
- ✅ **Backend Python** en servidor (Railway/VPS)
- ✅ **Frontend Web** en servidor (Railway/Vercel)
- ✅ **NUC Local** expuesto vía VPN (Tailscale/ZeroTier)
- ✅ Backend en servidor hace proxy al NUC local

📄 **📖 [Guía Completa de Configuración](backend/GUIA_CONFIGURACION_SERVIDOR.md)** ⭐

**Setup rápido (5 minutos):**
1. Instala Tailscale en NUC: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Obtén IP del NUC: `tailscale ip -4`
3. Configura en Railway: Variable `NUC_URL=http://IP_NUC:5000`
4. ¡Listo! El backend en servidor se conecta al NUC automáticamente

---

## 📚 **Otras Opciones de Conexión:**

📄 **Lee [Acceso Directo al NUC](backend/ACCESO_DIRECTO_NUC.md)** para más opciones:
- Tailscale (5 min, gratis) ⭐
- ZeroTier (5 min, gratis)
- IP Pública + Port Forwarding
- DDNS (No-IP)
- WireGuard VPN

---

## 📞 Soporte

**© 2025 Apptelink Vision**  
Versión 1.0.0

---

*Desarrollado con ❤️ usando React Native, Expo y Python Flask*

