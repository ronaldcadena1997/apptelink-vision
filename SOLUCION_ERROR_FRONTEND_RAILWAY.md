# 🔧 Solución: Error Frontend en Railway

## ❌ **Problema**
El frontend muestra error después de subir cambios a Railway.

---

## 🔍 **DIAGNÓSTICO PASO A PASO**

### **PASO 1: Verificar Logs en Railway**

1. **Ve a Railway → Servicio Frontend**
2. **Click en "Deployments" → Último deployment**
3. **Revisa los logs:**
   - ¿El build fue exitoso?
   - ¿Hay errores de dependencias?
   - ¿El servidor se inició correctamente?

**Errores comunes:**
- `Module not found` → Falta instalar dependencias
- `Command not found` → Comando incorrecto
- `Port already in use` → Puerto ocupado
- `Build failed` → Error en el build

---

## ✅ **SOLUCIONES**

### **Solución 1: Configuración Correcta para Railway**

**En Railway → Frontend Service → Settings → Build:**

```
Build Command: npm install && npm run build:web
Start Command: npx serve dist -s -p $PORT
```

**O si Railway usa Nixpacks automático:**
- Deja Build Command vacío
- Start Command: `npx serve dist -s -p $PORT`

**⚠️ IMPORTANTE:** 
- El comando `expo export --platform web` genera la carpeta `dist` (no `web-build`)
- Verifica en `vercel.json` que el `outputDirectory` es `dist`

---

### **Solución 2: Corregir package.json**

El comando `build:web` debe generar en `dist`:

```json
{
  "scripts": {
    "build:web": "expo export --platform web"
  }
}
```

**Verifica que `app.json` tenga:**
```json
{
  "expo": {
    "web": {
      "bundler": "metro"
    }
  }
}
```

---

### **Solución 3: Crear Dockerfile para Frontend (Alternativa)**

Si Railway no detecta correctamente el proyecto, crea un `Dockerfile.frontend`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Build del frontend
RUN npm run build:web

# Instalar serve para servir archivos estáticos
RUN npm install -g serve

# Exponer puerto
EXPOSE 8080

# Servir archivos estáticos
CMD ["serve", "-s", "dist", "-l", "8080"]
```

**En Railway:**
- Dockerfile Path: `Dockerfile.frontend`
- Root Directory: (vacío)

---

### **Solución 4: Usar Vercel (Recomendado para Expo)**

Vercel es más fácil y confiable para Expo:

1. **Ve a:** https://vercel.com
2. **Importa tu repositorio**
3. **Framework:** Expo (detecta automáticamente)
4. **Build Command:** (automático)
5. **Output Directory:** `dist` (según `vercel.json`)
6. **Deploy**

**Ventajas:**
- ✅ Configuración automática
- ✅ Mejor para Expo/React
- ✅ CDN global
- ✅ Más rápido

---

## 📋 **Checklist de Verificación**

- [ ] Logs del frontend en Railway muestran build exitoso
- [ ] Build Command: `npm install && npm run build:web`
- [ ] Start Command: `npx serve dist -s -p $PORT`
- [ ] La carpeta `dist` se genera después del build
- [ ] El puerto `$PORT` está configurado en Railway
- [ ] `vercel.json` tiene `outputDirectory: "dist"`

---

## 🆘 **Si Aún No Funciona**

### **1. Verifica el error específico:**
- Copia el error completo de los logs
- Compártelo para diagnóstico

### **2. Prueba localmente:**
```powershell
cd C:\Users\Administrator\Desktop\proyectowebApptelinkVision
npm install
npm run build:web
npx serve dist -s -p 3000
```
- Abre `http://localhost:3000`
- ¿Funciona localmente?

### **3. Verifica que los archivos están en Git:**
```powershell
git ls-files | findstr package.json
git ls-files | findstr app.json
```

### **4. Usa Vercel como alternativa:**
- Más fácil de configurar
- Mejor para Expo
- Menos problemas

---

**¡Con estas soluciones deberías poder resolver el error del frontend!** 🔧
