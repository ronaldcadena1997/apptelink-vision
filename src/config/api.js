// Configuración de la API
// IMPORTANTE: El backend debe estar en tu red local para acceder a las cámaras

// Detectar si estamos en web (producción) o móvil/local
const isWeb = typeof window !== 'undefined';
const isLocalhost = isWeb && window.location.hostname === 'localhost';

// Para producción web: usar túnel (ngrok/cloudflare) o backend local si estás en la misma red
// Para desarrollo local: usar IP local
// Para móviles: usar túnel o IP local si estás en la misma red

// CONFIGURACIÓN: Cambia esto según tu setup
// Opción 1: Backend local (mismo WiFi) - Para desarrollo local
const BACKEND_LOCAL = 'http://192.168.60.8:5000';

// Opción 2: Túnel ngrok/cloudflare - Para acceso remoto (opcional)
// Obtén la URL de tu túnel y reemplaza esta línea:
const BACKEND_TUNEL = null; // 'https://TU-TUNEL.ngrok-free.app'; // <-- Descomenta si usas túnel

// Opción 3: Backend en Railway (PRODUCCIÓN) - ✅ USA ESTE PARA PRODUCCIÓN
// ⚠️ IMPORTANTE: Reemplaza con la URL real de tu backend en Railway
// Obtén la URL en: Railway → Tu Servicio → Settings → Networking → Public Domain
const BACKEND_RAILWAY = 'https://apptelink-vision-production.up.railway.app';

// Seleccionar backend según el entorno
// Para producción web: usar Railway (el backend en Railway se conecta al NUC vía Tailscale)
// Para desarrollo local: usar IP local del NUC

// Detectar si estamos en producción (web) o desarrollo
const isProduction = isWeb && !isLocalhost && window.location.hostname !== 'localhost';

// Seleccionar backend automáticamente
let API_BASE_URL;
if (isProduction) {
  // Producción: usar Railway
  API_BASE_URL = BACKEND_RAILWAY;
  console.log('🌐 Usando backend en Railway:', BACKEND_RAILWAY);
} else {
  // Desarrollo: usar local o túnel
  API_BASE_URL = BACKEND_TUNEL || BACKEND_LOCAL;
  console.log('🏠 Usando backend local:', API_BASE_URL);
}

// Exportar la URL seleccionada
export { API_BASE_URL };

export const API_ENDPOINTS = {
  // Estado
  status: `${API_BASE_URL}/api/status`,
  obtenerIP: `${API_BASE_URL}/api/ip`,
  
  // Cámaras
  detectarCamaras: `${API_BASE_URL}/api/camaras/detectar`,
  listarCamaras: `${API_BASE_URL}/api/camaras`,
  snapshotCamara: (ip) => `${API_BASE_URL}/api/camaras/${ip}/snapshot`,
  snapshotBase64: (ip) => `${API_BASE_URL}/api/camaras/${ip}/snapshot/base64`,
  
  // Cercas (por cámara)
  listarTodasCercas: `${API_BASE_URL}/api/cercas`,
  obtenerCercas: (ip) => `${API_BASE_URL}/api/cercas/${ip}`,
  guardarCercas: (ip) => `${API_BASE_URL}/api/cercas/${ip}`,
  eliminarCerca: (ip, nombre) => `${API_BASE_URL}/api/cercas/${ip}/${nombre}`,
  
  // Intrusos
  listarIntrusos: `${API_BASE_URL}/api/intrusos`,
  obtenerImagen: (archivo) => `${API_BASE_URL}/api/intrusos/${archivo}`,
  obtenerImagenBase64: (archivo) => `${API_BASE_URL}/api/intrusos/${archivo}/base64`,
  eliminarImagen: (archivo) => `${API_BASE_URL}/api/intrusos/${archivo}`,
  
  // Videos de intrusión
  listarVideos: `${API_BASE_URL}/api/videos`,
  obtenerVideo: (archivo) => `${API_BASE_URL}/api/videos/${archivo}`,
  eliminarVideo: (archivo) => `${API_BASE_URL}/api/videos/${archivo}`,
  
  // Ejecutar scripts
  ejecutarDetectarCamaras: `${API_BASE_URL}/api/ejecutar/detectar-camaras`,
  ejecutarConfigurarCercas: `${API_BASE_URL}/api/ejecutar/configurar-cercas`,
  ejecutarVigilancia: (ip) => `${API_BASE_URL}/api/ejecutar/vigilancia/${ip}`,
  ejecutarMonitoreo: `${API_BASE_URL}/api/ejecutar/monitoreo`,
  ejecutarMonitoreoCercas: `${API_BASE_URL}/api/ejecutar/monitoreo-cercas`,
};

// Helper para hacer peticiones
export const fetchAPI = async (url, options = {}) => {
  try {
    console.log('📡 Petición a:', url);
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      console.error('❌ Error HTTP:', response.status, response.statusText);
      const errorText = await response.text();
      console.error('❌ Respuesta:', errorText);
      return { success: false, error: `HTTP ${response.status}: ${response.statusText}` };
    }
    
    const data = await response.json();
    console.log('✅ Respuesta exitosa:', data);
    return data;
  } catch (error) {
    console.error('❌ Error en API:', error);
    console.error('❌ URL que falló:', url);
    return { success: false, error: error.message };
  }
};

// Función para detectar automáticamente la IP del backend
export const detectarIPBackend = async () => {
  // Lista de posibles IPs/URLs a probar (en orden de prioridad)
  const posiblesBackends = [
    BACKEND_RAILWAY, // Primero probar Railway (producción)
    BACKEND_TUNEL,
    BACKEND_LOCAL,
    'http://192.168.60.8:5000', // IP local del NUC
    'http://100.92.50.72:5000', // IP Tailscale del NUC (directo, no recomendado)
  ].filter(Boolean); // Eliminar valores undefined/null

  console.log('🔍 Detectando IP del backend...');

  // Probar cada backend
  for (const backendUrl of posiblesBackends) {
    try {
      const response = await fetch(`${backendUrl}/api/status`, {
        method: 'GET',
        timeout: 3000,
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'online') {
          console.log(`✅ Backend detectado en: ${backendUrl}`);
          return backendUrl;
        }
      }
    } catch (error) {
      // Continuar con el siguiente
      continue;
    }
  }

  console.warn('⚠️ No se pudo detectar el backend automáticamente');
  return null;
};

// Función para obtener información de IPs del backend
export const obtenerInfoIP = async (backendUrl) => {
  try {
    const response = await fetch(`${backendUrl}/api/ip`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error obteniendo info de IP:', error);
    return null;
  }
};

