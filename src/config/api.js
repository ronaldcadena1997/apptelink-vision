// Configuración de la API
// Cambiar esta IP a la IP del servidor donde corre el backend Python

export const API_BASE_URL = 'http://192.168.60.15:5000';

export const API_ENDPOINTS = {
  // Estado
  status: `${API_BASE_URL}/api/status`,
  
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
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    return await response.json();
  } catch (error) {
    console.error('Error en API:', error);
    return { success: false, error: error.message };
  }
};

