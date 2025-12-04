import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Platform,
  Alert,
  Image,
  ActivityIndicator,
  Dimensions,
  Modal,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { API_ENDPOINTS, fetchAPI, API_BASE_URL } from '../config/api';

const { width: screenWidth } = Dimensions.get('window');

const COLORES = ['#FFFF00', '#FFA500', '#FF00FF', '#00FFFF', '#00FF00', '#FF0000', '#0000FF'];

export default function MonitoreoScreen({ route }) {
  const { conCercas } = route.params || {};
  const [camaras, setCamaras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activo, setActivo] = useState(false);
  const [cercasCamaras, setCercasCamaras] = useState({});
  const [camaraFullscreen, setCamaraFullscreen] = useState(null);
  const [streamingActivo, setStreamingActivo] = useState({});

  useEffect(() => {
    cargarCamaras();
  }, []);

  const cargarCamaras = async () => {
    setLoading(true);
    const response = await fetchAPI(API_ENDPOINTS.listarCamaras);
    
    if (response.success && response.camaras) {
      setCamaras(response.camaras);
      
      // Si es con cercas, cargar cercas de cada cámara
      if (conCercas) {
        const cercasTemp = {};
        for (const cam of response.camaras) {
          const cercasResponse = await fetchAPI(API_ENDPOINTS.obtenerCercas(cam.ip));
          if (cercasResponse.success) {
            cercasTemp[cam.ip] = cercasResponse.cercas || [];
          }
        }
        setCercasCamaras(cercasTemp);
      }
    }
    setLoading(false);
  };

  const iniciarMonitoreo = () => {
    setActivo(true);
  };

  const detenerMonitoreo = () => {
    setActivo(false);
  };

  const verSector = (camara) => {
    setCamaraFullscreen(camara);
    // Iniciar streaming individual
    setStreamingActivo(prev => ({ ...prev, [camara.ip]: true }));
  };

  const cerrarFullscreen = () => {
    if (camaraFullscreen) {
      // Detener streaming individual
      setStreamingActivo(prev => ({ ...prev, [camaraFullscreen.ip]: false }));
    }
    setCamaraFullscreen(null);
  };

  const toggleStreamingIndividual = (ip) => {
    setStreamingActivo(prev => ({
      ...prev,
      [ip]: !prev[ip]
    }));
  };

  const renderLineasCamara = (ip) => {
    if (!conCercas || !cercasCamaras[ip] || cercasCamaras[ip].length === 0) {
      return null;
    }

    return (
      <svg 
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: 10,
          pointerEvents: 'none',
        }}
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
      >
        {cercasCamaras[ip].map((cerca, index) => {
          const color = COLORES[cerca.color_index % COLORES.length];
          
          return (
            <g key={index}>
              <line
                x1={cerca.x1}
                y1={cerca.y1}
                x2={cerca.x2}
                y2={cerca.y2}
                stroke={color}
                strokeWidth="0.5"
                strokeLinecap="round"
              />
              <circle cx={cerca.x1} cy={cerca.y1} r="0.8" fill={color} stroke="#000" strokeWidth="0.1" />
              <circle cx={cerca.x2} cy={cerca.y2} r="0.8" fill={color} stroke="#000" strokeWidth="0.1" />
              <text
                x={(cerca.x1 + cerca.x2) / 2}
                y={(cerca.y1 + cerca.y2) / 2}
                fill={color}
                fontSize="2.5"
                fontWeight="bold"
                textAnchor="middle"
                stroke="#000"
                strokeWidth="0.1"
                paintOrder="stroke"
              >
                {cerca.nombre}
              </text>
            </g>
          );
        })}
      </svg>
    );
  };

  return (
    <View style={styles.container}>
      {/* Modal para pantalla completa */}
      <Modal
        visible={camaraFullscreen !== null}
        animationType="fade"
        onRequestClose={cerrarFullscreen}
      >
        <View style={styles.fullscreenContainer}>
          {/* Header del modal */}
          <View style={styles.fullscreenHeader}>
            <View style={styles.fullscreenInfo}>
              <Text style={styles.fullscreenTitle}>{camaraFullscreen?.nombre}</Text>
              <Text style={styles.fullscreenIP}>{camaraFullscreen?.ip}</Text>
            </View>
            <TouchableOpacity
              style={styles.closeButton}
              onPress={cerrarFullscreen}
            >
              <Ionicons name="close" size={24} color="#fff" />
            </TouchableOpacity>
          </View>

          {/* Stream en pantalla completa */}
          <View style={styles.fullscreenVideo}>
            {camaraFullscreen && streamingActivo[camaraFullscreen.ip] && (
              <View style={{ width: '100%', height: '100%', position: 'relative' }}>
                <Image
                  source={{ uri: `${API_BASE_URL}/api/camaras/${camaraFullscreen.ip}/stream?t=${Date.now()}` }}
                  style={styles.fullscreenImage}
                  resizeMode="contain"
                />
                {/* Líneas de cercas en pantalla completa */}
                {conCercas && Platform.OS === 'web' && renderLineasCamara(camaraFullscreen.ip)}
              </View>
            )}
          </View>

          {/* Controles */}
          <View style={styles.fullscreenControls}>
            <TouchableOpacity
              style={[
                styles.fullscreenControlButton,
                streamingActivo[camaraFullscreen?.ip || ''] ? styles.stopButton : styles.startButton
              ]}
              onPress={() => camaraFullscreen && toggleStreamingIndividual(camaraFullscreen.ip)}
            >
              <Ionicons
                name={streamingActivo[camaraFullscreen?.ip || ''] ? "stop" : "play"}
                size={20}
                color="#fff"
              />
              <Text style={styles.fullscreenControlText}>
                {streamingActivo[camaraFullscreen?.ip || ''] ? 'DETENER' : 'INICIAR'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.headerCard}>
          <View style={styles.headerIconContainer}>
            <Ionicons 
              name={conCercas ? "grid" : "apps"} 
              size={40} 
              color={conCercas ? "#2ed573" : "#00d4ff"} 
            />
          </View>
          <View style={styles.headerInfo}>
            <Text style={styles.headerTitle}>
              {conCercas ? 'Monitoreo con Cercas' : 'Monitoreo General'}
            </Text>
            <Text style={styles.headerSubtitle}>
              {camaras.length} {camaras.length === 1 ? 'cámara' : 'cámaras'} detectadas
            </Text>
          </View>
        </View>

        {/* Botón de control */}
        {!loading && camaras.length > 0 && (
          <TouchableOpacity
            style={[
              styles.controlButton,
              activo ? styles.stopButton : styles.startButton,
              { backgroundColor: activo ? '#ff4757' : (conCercas ? '#2ed573' : '#00d4ff') }
            ]}
            onPress={activo ? detenerMonitoreo : iniciarMonitoreo}
          >
            <Ionicons 
              name={activo ? "stop" : "play"} 
              size={24} 
              color="#fff" 
            />
            <Text style={styles.controlButtonText}>
              {activo ? 'DETENER MONITOREO' : 'INICIAR MONITOREO'}
            </Text>
          </TouchableOpacity>
        )}

        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#00d4ff" />
            <Text style={styles.loadingText}>Cargando cámaras...</Text>
          </View>
        ) : camaras.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="videocam-off" size={80} color="#3a4a6a" />
            <Text style={styles.emptyText}>No hay cámaras disponibles</Text>
            <Text style={styles.emptySubtext}>
              Detecta cámaras desde "Cámara de Vigilancia"
            </Text>
          </View>
        ) : (
          <>
            {/* Grid de cámaras */}
            <View style={styles.camerasGrid}>
              {camaras.map((camara, index) => (
                <View key={index} style={styles.cameraCell}>
                  {/* Header de la cámara */}
                  <View style={styles.cameraHeader}>
                    <Text style={styles.cameraName}>{camara.nombre}</Text>
                    <Text style={styles.cameraIP}>{camara.ip}</Text>
                    {(activo || streamingActivo[camara.ip]) && (
                      <View style={styles.liveIndicator}>
                        <View style={styles.liveDot} />
                        <Text style={styles.liveText}>EN VIVO</Text>
                      </View>
                    )}
                  </View>

                  {/* Stream de video */}
                  <View style={styles.videoContainer}>
                    {(activo || streamingActivo[camara.ip]) ? (
                      <View style={{ width: '100%', height: '100%', position: 'relative' }}>
                        <Image
                          source={{ uri: `${API_BASE_URL}/api/camaras/${camara.ip}/stream?t=${Date.now()}` }}
                          style={styles.streamImage}
                          resizeMode="contain"
                        />
                        {/* Líneas de cercas */}
                        {conCercas && Platform.OS === 'web' && renderLineasCamara(camara.ip)}
                      </View>
                    ) : (
                      <View style={styles.cameraPlaceholder}>
                        <Ionicons name="videocam" size={60} color="#3a4a6a" />
                        <Text style={styles.placeholderText}>
                          Presiona "Iniciar" para ver
                        </Text>
                      </View>
                    )}
                  </View>

                  {/* Botón Ver Sector */}
                  <TouchableOpacity
                    style={styles.verSectorButton}
                    onPress={() => verSector(camara)}
                  >
                    <Ionicons name="expand" size={16} color="#fff" />
                    <Text style={styles.verSectorText}>VER SECTOR</Text>
                  </TouchableOpacity>

                  {/* Footer con info */}
                  <View style={styles.cameraFooter}>
                    <View style={[
                      styles.statusDot,
                      { backgroundColor: camara.estado === 'activa' ? '#2ed573' : '#ff4757' }
                    ]} />
                    <Text style={styles.statusText}>
                      {camara.estado === 'activa' ? 'Operativa' : 'Sin acceso'}
                    </Text>
                    {conCercas && cercasCamaras[camara.ip] && (
                      <Text style={styles.cercasCount}>
                        {cercasCamaras[camara.ip].length} cercas
                      </Text>
                    )}
                  </View>
                </View>
              ))}
            </View>

            {/* Instrucciones */}
            {!activo && Object.values(streamingActivo).every(v => !v) && (
              <View style={styles.instructionsCard}>
                <Text style={styles.instructionsTitle}>💡 Modo de uso</Text>
                <Text style={styles.instructionText}>
                  • Presiona "INICIAR MONITOREO" para ver todas las cámaras en vivo
                </Text>
                <Text style={styles.instructionText}>
                  • O presiona "VER SECTOR" en una cámara para verla individualmente
                </Text>
                <Text style={styles.instructionText}>
                  • Las cámaras se actualizarán en tiempo real
                </Text>
                {conCercas && (
                  <Text style={styles.instructionText}>
                    • Las líneas de detección aparecerán sobre cada cámara
                  </Text>
                )}
                <Text style={styles.instructionText}>
                  • Presiona "DETENER" para pausar el monitoreo general
                </Text>
                <Text style={styles.instructionText}>
                  • El streaming individual se detiene automáticamente al cerrar
                </Text>
              </View>
            )}
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a1628',
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  headerCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(20, 35, 60, 0.8)',
    borderRadius: 20,
    padding: 20,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.2)',
  },
  headerIconContainer: {
    width: 70,
    height: 70,
    backgroundColor: 'rgba(0, 212, 255, 0.15)',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  headerInfo: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerSubtitle: {
    fontSize: 13,
    color: '#5a6a8a',
    marginTop: 4,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 12,
    height: 55,
    gap: 10,
    marginBottom: 20,
  },
  startButton: {
    backgroundColor: '#00d4ff',
  },
  stopButton: {
    backgroundColor: '#ff4757',
  },
  controlButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    color: '#5a6a8a',
    marginTop: 15,
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 60,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 20,
  },
  emptySubtext: {
    fontSize: 13,
    color: '#5a6a8a',
    textAlign: 'center',
    marginTop: 10,
  },
  camerasGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 15,
    marginBottom: 20,
  },
  cameraCell: {
    width: screenWidth > 800 ? (screenWidth - 70) / 2 : screenWidth - 40,
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.2)',
  },
  cameraHeader: {
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  cameraName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  cameraIP: {
    fontSize: 11,
    color: '#5a6a8a',
  },
  liveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 0, 0, 0.2)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  liveDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#ff0000',
    marginRight: 5,
  },
  liveText: {
    fontSize: 9,
    fontWeight: 'bold',
    color: '#ff0000',
  },
  videoContainer: {
    width: '100%',
    height: 200,
    backgroundColor: '#000',
    position: 'relative',
  },
  streamImage: {
    width: '100%',
    height: '100%',
  },
  cameraPlaceholder: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
  },
  placeholderText: {
    color: '#5a6a8a',
    fontSize: 12,
    marginTop: 10,
  },
  cameraFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  statusText: {
    fontSize: 11,
    color: '#8a9ab0',
    flex: 1,
  },
  cercasCount: {
    fontSize: 10,
    color: '#00d4ff',
    backgroundColor: 'rgba(0, 212, 255, 0.2)',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  instructionsCard: {
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    padding: 20,
  },
  instructionsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 12,
  },
  instructionText: {
    fontSize: 13,
    color: '#8a9ab0',
    marginBottom: 8,
    lineHeight: 20,
  },
  verSectorButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#00d4ff',
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginHorizontal: 10,
    marginBottom: 8,
    borderRadius: 6,
    gap: 6,
  },
  verSectorText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  fullscreenContainer: {
    flex: 1,
    backgroundColor: '#000',
  },
  fullscreenHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    padding: 20,
    paddingTop: 50,
  },
  fullscreenInfo: {
    flex: 1,
  },
  fullscreenTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  fullscreenIP: {
    fontSize: 14,
    color: '#5a6a8a',
    marginTop: 4,
  },
  closeButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255, 71, 87, 0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  fullscreenVideo: {
    flex: 1,
    backgroundColor: '#000',
  },
  fullscreenImage: {
    width: '100%',
    height: '100%',
  },
  fullscreenControls: {
    padding: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
  },
  fullscreenControlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 10,
    height: 50,
    gap: 10,
  },
  fullscreenControlText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
