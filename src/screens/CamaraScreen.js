import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
  ActivityIndicator,
  Alert,
  Image,
  RefreshControl,
  Platform,
  Modal,
  StatusBar,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { API_ENDPOINTS, fetchAPI, API_BASE_URL } from '../config/api';

const { width, height } = Dimensions.get('window');

export default function CamaraScreen() {
  const [camaras, setCamaras] = useState([]);
  const [camaraSeleccionada, setCamaraSeleccionada] = useState(null);
  const [loading, setLoading] = useState(false);
  const [escaneando, setEscaneando] = useState(false);
  const [snapshot, setSnapshot] = useState(null);
  const [loadingSnapshot, setLoadingSnapshot] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [infoRed, setInfoRed] = useState(null);
  const [streamActivo, setStreamActivo] = useState(false);
  const [streamKey, setStreamKey] = useState(0);
  const [fullscreen, setFullscreen] = useState(false);
  const [mostrarSector, setMostrarSector] = useState(false);
  const [cercasSector, setCercasSector] = useState([]);
  const streamRef = useRef(null);

  // Cargar cámaras al iniciar
  useEffect(() => {
    cargarCamaras();
  }, []);

  const cargarCamaras = async () => {
    setLoading(true);
    const response = await fetchAPI(API_ENDPOINTS.listarCamaras);
    if (response.success) {
      setCamaras(response.camaras || []);
      if (response.camaras?.length > 0) {
        setCamaraSeleccionada(response.camaras[0]);
      }
    }
    setLoading(false);
  };

  const detectarCamaras = async () => {
    setEscaneando(true);
    Alert.alert(
      'Escaneando Red',
      'Buscando cámaras en la red local...\nEsto puede tomar 1-2 minutos.',
      [{ text: 'OK' }]
    );

    const response = await fetchAPI(API_ENDPOINTS.detectarCamaras);
    
    if (response.success) {
      setCamaras(response.camaras || []);
      setInfoRed({
        ip_local: response.ip_local,
        red: response.red,
        total_dispositivos: response.total_dispositivos,
      });
      
      if (response.camaras?.length > 0) {
        setCamaraSeleccionada(response.camaras[0]);
        Alert.alert(
          'Escaneo Completado',
          `Se encontraron ${response.camaras.length} cámara(s) en la red ${response.red}`
        );
      } else {
        Alert.alert(
          'Escaneo Completado',
          'No se encontraron cámaras activas en la red'
        );
      }
    } else {
      Alert.alert('Error', response.error || 'No se pudo completar el escaneo');
    }
    
    setEscaneando(false);
  };

  const capturarSnapshot = async () => {
    if (!camaraSeleccionada?.ip) return;
    
    setLoadingSnapshot(true);
    const response = await fetchAPI(API_ENDPOINTS.snapshotCamara(camaraSeleccionada.ip));
    
    if (response.success) {
      setSnapshot(response.image);
    } else {
      Alert.alert('Error', 'No se pudo capturar la imagen');
    }
    setLoadingSnapshot(false);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await cargarCamaras();
    setRefreshing(false);
  };

  const iniciarStream = () => {
    if (camaraSeleccionada?.ip && camaraSeleccionada.estado === 'activa') {
      setStreamActivo(true);
      setMostrarSector(false);
      setSnapshot(null);
      setStreamKey(prev => prev + 1);
    }
  };

  const iniciarStreamConSector = async () => {
    if (camaraSeleccionada?.ip && camaraSeleccionada.estado === 'activa') {
      // Cargar cercas de la cámara
      const response = await fetchAPI(`${API_BASE_URL}/api/cercas/${camaraSeleccionada.ip}`);
      if (response.success) {
        setCercasSector(response.cercas || []);
        
        // Ejecutar el script Python de vigilancia
        const vigilanciaResponse = await fetchAPI(API_ENDPOINTS.ejecutarVigilancia(camaraSeleccionada.ip), {
          method: 'POST',
        });
        
        if (vigilanciaResponse.success) {
          console.log('Vigilancia iniciada:', vigilanciaResponse.message);
        }
      }
      setStreamActivo(true);
      setMostrarSector(true);
      setSnapshot(null);
      setStreamKey(prev => prev + 1);
      // Abrir en pantalla completa automáticamente
      setFullscreen(true);
    }
  };

  const detenerStream = async () => {
    if (camaraSeleccionada?.ip) {
      setStreamActivo(false);
      await fetchAPI(`${API_BASE_URL}/api/camaras/${camaraSeleccionada.ip}/stream/stop`, {
        method: 'POST',
      });
    }
  };

  const seleccionarCamara = (camara) => {
    // Detener stream anterior si existe
    if (streamActivo && camaraSeleccionada?.ip) {
      detenerStream();
    }
    setCamaraSeleccionada(camara);
    setSnapshot(null);
    setStreamActivo(false);
  };

  // Limpiar stream al desmontar
  useEffect(() => {
    return () => {
      if (camaraSeleccionada?.ip) {
        fetchAPI(`${API_BASE_URL}/api/camaras/${camaraSeleccionada.ip}/stream/stop`, {
          method: 'POST',
        });
      }
    };
  }, []);

  const abrirFullscreen = () => {
    if (camaraSeleccionada?.ip && camaraSeleccionada.estado === 'activa') {
      if (!streamActivo) {
        iniciarStream();
      }
      setFullscreen(true);
    }
  };

  const cerrarFullscreen = async () => {
    setFullscreen(false);
    // Si se estaba viendo un sector, detener el streaming al cerrar
    if (mostrarSector) {
      await detenerStream();
      setMostrarSector(false);
      setCercasSector([]);
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#00d4ff" />
        }
      >
        {/* Botón de escaneo */}
        <TouchableOpacity
          style={[styles.scanButton, escaneando && styles.scanButtonDisabled]}
          onPress={detectarCamaras}
          disabled={escaneando}
        >
          {escaneando ? (
            <>
              <ActivityIndicator color="#0a1628" size="small" />
              <Text style={styles.scanButtonText}>ESCANEANDO RED...</Text>
            </>
          ) : (
            <>
              <Ionicons name="search" size={22} color="#0a1628" />
              <Text style={styles.scanButtonText}>DETECTAR CÁMARAS EN LA RED</Text>
            </>
          )}
        </TouchableOpacity>

        {/* Info de red */}
        {infoRed && (
          <View style={styles.infoRedContainer}>
            <View style={styles.infoRedItem}>
              <Ionicons name="wifi" size={16} color="#00d4ff" />
              <Text style={styles.infoRedText}>IP Local: {infoRed.ip_local}</Text>
            </View>
            <View style={styles.infoRedItem}>
              <Ionicons name="globe" size={16} color="#2ed573" />
              <Text style={styles.infoRedText}>Red: {infoRed.red}</Text>
            </View>
          </View>
        )}

        {/* Visor de cámara principal */}
        <View style={styles.mainViewer}>
          <View style={styles.cameraPlaceholder}>
            {streamActivo && camaraSeleccionada?.ip ? (
              // Stream de video en vivo
              <View style={styles.streamContainer}>
                <Image
                  key={streamKey}
                  source={{ uri: `${API_BASE_URL}/api/camaras/${camaraSeleccionada.ip}/stream?t=${streamKey}` }}
                  style={styles.streamImage}
                  resizeMode="contain"
                  onError={() => {
                    console.log('Error en stream');
                  }}
                />
                {/* Líneas de sector superpuestas */}
                {mostrarSector && cercasSector.length > 0 && Platform.OS === 'web' && (
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
                    {cercasSector.map((cerca, index) => {
                      const COLORES = ['#FFFF00', '#FFA500', '#FF00FF', '#00FFFF', '#00FF00', '#FF0000', '#0000FF'];
                      const color = COLORES[cerca.color_index % COLORES.length];
                      
                      return (
                        <g key={index}>
                          {/* Línea */}
                          <line
                            x1={cerca.x1}
                            y1={cerca.y1}
                            x2={cerca.x2}
                            y2={cerca.y2}
                            stroke={color}
                            strokeWidth="0.5"
                            strokeLinecap="round"
                          />
                          {/* Punto inicio */}
                          <circle cx={cerca.x1} cy={cerca.y1} r="0.8" fill={color} stroke="#000" strokeWidth="0.1" />
                          {/* Punto fin */}
                          <circle cx={cerca.x2} cy={cerca.y2} r="0.8" fill={color} stroke="#000" strokeWidth="0.1" />
                          {/* Etiqueta */}
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
                )}
                <View style={styles.liveIndicatorStream}>
                  <View style={styles.liveDotRecording} />
                  <Text style={styles.liveTextRecording}>
                    {mostrarSector ? '● SECTOR EN VIVO' : '● EN VIVO'}
                  </Text>
                </View>
              </View>
            ) : loadingSnapshot ? (
              <ActivityIndicator size="large" color="#00d4ff" />
            ) : snapshot ? (
              <Image
                source={{ uri: snapshot }}
                style={styles.snapshotImage}
                resizeMode="contain"
              />
            ) : (
              <>
                <Ionicons name="videocam" size={60} color="#00d4ff" />
                <Text style={styles.cameraName}>
                  {camaraSeleccionada?.nombre || 'Sin cámara seleccionada'}
                </Text>
                <Text style={styles.cameraLocation}>
                  {camaraSeleccionada?.ip || 'Escanea la red para detectar cámaras'}
                </Text>
                {camaraSeleccionada?.estado === 'activa' && (
                  <View style={styles.playButtonsContainer}>
                    <TouchableOpacity style={styles.playButton} onPress={iniciarStream}>
                      <Ionicons name="play-circle" size={50} color="#00d4ff" />
                      <Text style={styles.playButtonText}>Ver en vivo</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.playButtonSector} onPress={() => iniciarStreamConSector()}>
                      <Ionicons name="scan" size={50} color="#ff6b35" />
                      <Text style={styles.playButtonTextSector}>Ver sector</Text>
                    </TouchableOpacity>
                  </View>
                )}
              </>
            )}
            
            {camaraSeleccionada && !streamActivo && (
              <View style={styles.liveIndicator}>
                <View style={[
                  styles.liveDot,
                  { backgroundColor: camaraSeleccionada.estado === 'activa' ? '#2ed573' : '#ff4757' }
                ]} />
                <Text style={styles.liveText}>
                  {camaraSeleccionada.estado === 'activa' ? 'ACTIVA' : 'SIN ACCESO'}
                </Text>
              </View>
            )}
          </View>

          {/* Controles de cámara */}
          {camaraSeleccionada && (
            <View style={styles.controlsRow}>
              {streamActivo ? (
                <TouchableOpacity
                  style={[styles.controlButton, styles.stopButton]}
                  onPress={detenerStream}
                >
                  <Ionicons name="stop-circle" size={24} color="#ff4757" />
                  <Text style={[styles.controlText, { color: '#ff4757' }]}>Detener</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity
                  style={styles.controlButton}
                  onPress={iniciarStream}
                  disabled={camaraSeleccionada.estado !== 'activa'}
                >
                  <Ionicons name="play" size={24} color={camaraSeleccionada.estado === 'activa' ? '#2ed573' : '#5a6a8a'} />
                  <Text style={styles.controlText}>En Vivo</Text>
                </TouchableOpacity>
              )}

              <TouchableOpacity
                style={styles.controlButton}
                onPress={capturarSnapshot}
                disabled={loadingSnapshot || camaraSeleccionada.estado !== 'activa'}
              >
                <Ionicons name="camera" size={24} color="#ffffff" />
                <Text style={styles.controlText}>Capturar</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={styles.controlButton}
                onPress={() => {
                  setStreamKey(prev => prev + 1);
                  if (!streamActivo) iniciarStream();
                }}
              >
                <Ionicons name="refresh" size={24} color="#ffffff" />
                <Text style={styles.controlText}>Actualizar</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={styles.controlButton}
                onPress={abrirFullscreen}
                disabled={camaraSeleccionada.estado !== 'activa'}
              >
                <Ionicons name="expand" size={24} color={camaraSeleccionada.estado === 'activa' ? '#00d4ff' : '#5a6a8a'} />
                <Text style={styles.controlText}>Pantalla Completa</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={styles.controlButton}
                onPress={() => {
                  Alert.alert(
                    camaraSeleccionada.nombre,
                    `IP: ${camaraSeleccionada.ip}\nResolución: ${camaraSeleccionada.resolucion || 'N/A'}\nEstado: ${camaraSeleccionada.estado}`
                  );
                }}
              >
                <Ionicons name="information-circle" size={24} color="#ffffff" />
                <Text style={styles.controlText}>Info</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>

        {/* Lista de cámaras */}
        <View style={styles.cameraListSection}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Cámaras Detectadas</Text>
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{camaras.length}</Text>
            </View>
          </View>

          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#00d4ff" />
              <Text style={styles.loadingText}>Cargando cámaras...</Text>
            </View>
          ) : camaras.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="videocam-off" size={50} color="#3a4a6a" />
              <Text style={styles.emptyText}>No hay cámaras detectadas</Text>
              <Text style={styles.emptySubtext}>
                Presiona "Detectar Cámaras" para buscar en la red
              </Text>
            </View>
          ) : (
            <View style={styles.cameraGrid}>
              {camaras.map((camara) => (
                <TouchableOpacity
                  key={camara.id}
                  style={[
                    styles.cameraCard,
                    camaraSeleccionada?.id === camara.id && styles.cameraCardSelected,
                    camara.estado !== 'activa' && styles.cameraCardInactive,
                  ]}
                  onPress={() => seleccionarCamara(camara)}
                >
                  <View style={styles.cameraThumbnail}>
                    <Ionicons
                      name="videocam"
                      size={30}
                      color={camara.estado === 'activa' ? '#00d4ff' : '#5a6a8a'}
                    />
                  </View>
                  <View style={styles.cameraInfo}>
                    <Text style={styles.cameraCardName}>{camara.nombre}</Text>
                    <Text style={styles.cameraCardLocation}>IP: {camara.ip}</Text>
                    {camara.resolucion && (
                      <Text style={styles.cameraResolution}>{camara.resolucion}</Text>
                    )}
                  </View>
                  <View
                    style={[
                      styles.statusBadge,
                      camara.estado === 'activa'
                        ? styles.statusActive
                        : styles.statusInactive,
                    ]}
                  >
                    <Text
                      style={[
                        styles.statusBadgeText,
                        camara.estado !== 'activa' && styles.statusTextInactive,
                      ]}
                    >
                      {camara.estado === 'activa' ? 'Activa' : 'Sin acceso'}
                    </Text>
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          )}
        </View>

        {/* Información adicional */}
        <View style={styles.infoSection}>
          <View style={styles.infoItem}>
            <Ionicons name="information-circle" size={20} color="#00d4ff" />
            <Text style={styles.infoText}>
              Las cámaras se detectan automáticamente en la red local
            </Text>
          </View>
          {/* Credenciales ocultas por seguridad */}
        </View>
      </ScrollView>

      {/* Modal de Pantalla Completa */}
      <Modal
        visible={fullscreen}
        animationType="fade"
        supportedOrientations={['portrait', 'landscape']}
        onRequestClose={cerrarFullscreen}
      >
        <View style={styles.fullscreenContainer}>
          <StatusBar hidden={fullscreen} />
          
          {/* Stream en pantalla completa */}
          {camaraSeleccionada?.ip && (
            <View style={{ flex: 1, width: '100%' }}>
              <Image
                key={`fullscreen-${streamKey}`}
                source={{ uri: `${API_BASE_URL}/api/camaras/${camaraSeleccionada.ip}/stream?t=${streamKey}` }}
                style={styles.fullscreenImage}
                resizeMode="contain"
              />
              {/* Líneas de sector en pantalla completa */}
              {mostrarSector && cercasSector.length > 0 && Platform.OS === 'web' && (
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
                  {cercasSector.map((cerca, index) => {
                    const COLORES = ['#FFFF00', '#FFA500', '#FF00FF', '#00FFFF', '#00FF00', '#FF0000', '#0000FF'];
                    const color = COLORES[cerca.color_index % COLORES.length];
                    
                    return (
                      <g key={index}>
                        {/* Línea */}
                        <line
                          x1={cerca.x1}
                          y1={cerca.y1}
                          x2={cerca.x2}
                          y2={cerca.y2}
                          stroke={color}
                          strokeWidth="0.8"
                          strokeLinecap="round"
                        />
                        {/* Punto inicio */}
                        <circle cx={cerca.x1} cy={cerca.y1} r="1.2" fill={color} stroke="#000" strokeWidth="0.2" />
                        {/* Punto fin */}
                        <circle cx={cerca.x2} cy={cerca.y2} r="1.2" fill={color} stroke="#000" strokeWidth="0.2" />
                        {/* Etiqueta */}
                        <text
                          x={(cerca.x1 + cerca.x2) / 2}
                          y={(cerca.y1 + cerca.y2) / 2}
                          fill={color}
                          fontSize="3"
                          fontWeight="bold"
                          textAnchor="middle"
                          stroke="#000"
                          strokeWidth="0.15"
                          paintOrder="stroke"
                        >
                          {cerca.nombre}
                        </text>
                      </g>
                    );
                  })}
                </svg>
              )}
            </View>
          )}

          {/* Overlay con controles */}
          <View style={styles.fullscreenOverlay}>
            {/* Header */}
            <View style={styles.fullscreenHeader}>
              <View style={styles.fullscreenLiveIndicator}>
                <View style={styles.fullscreenLiveDot} />
                <Text style={styles.fullscreenLiveText}>
                  {mostrarSector ? '● SECTOR EN VIVO' : '● EN VIVO'}
                </Text>
              </View>
              <Text style={styles.fullscreenCameraName}>
                {camaraSeleccionada?.nombre} - {camaraSeleccionada?.ip}
              </Text>
              <TouchableOpacity
                style={styles.fullscreenCloseButton}
                onPress={cerrarFullscreen}
              >
                <Ionicons name="close" size={30} color="#ffffff" />
              </TouchableOpacity>
            </View>

            {/* Footer con controles */}
            <View style={styles.fullscreenFooter}>
              <TouchableOpacity
                style={styles.fullscreenControlButton}
                onPress={capturarSnapshot}
              >
                <Ionicons name="camera" size={28} color="#ffffff" />
                <Text style={styles.fullscreenControlText}>Capturar</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.fullscreenControlButton}
                onPress={() => setStreamKey(prev => prev + 1)}
              >
                <Ionicons name="refresh" size={28} color="#ffffff" />
                <Text style={styles.fullscreenControlText}>Actualizar</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.fullscreenControlButton, styles.fullscreenStopButton]}
                onPress={() => {
                  detenerStream();
                  cerrarFullscreen();
                }}
              >
                <Ionicons name="stop-circle" size={28} color="#ff4757" />
                <Text style={[styles.fullscreenControlText, { color: '#ff4757' }]}>Detener</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.fullscreenControlButton}
                onPress={cerrarFullscreen}
              >
                <Ionicons name="contract" size={28} color="#00d4ff" />
                <Text style={[styles.fullscreenControlText, { color: '#00d4ff' }]}>Salir</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
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
  scanButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#00d4ff',
    borderRadius: 12,
    height: 55,
    marginBottom: 15,
    gap: 10,
  },
  scanButtonDisabled: {
    backgroundColor: '#2a5a6a',
  },
  scanButtonText: {
    color: '#0a1628',
    fontSize: 14,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  infoRedContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 10,
    padding: 12,
    marginBottom: 15,
  },
  infoRedItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  infoRedText: {
    color: '#8a9ab0',
    fontSize: 12,
  },
  mainViewer: {
    backgroundColor: 'rgba(20, 35, 60, 0.8)',
    borderRadius: 20,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.2)',
    marginBottom: 20,
  },
  cameraPlaceholder: {
    height: 220,
    backgroundColor: '#0d1f38',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  snapshotImage: {
    width: '100%',
    height: '100%',
  },
  streamContainer: {
    width: '100%',
    height: '100%',
    position: 'relative',
  },
  streamImage: {
    width: '100%',
    height: '100%',
    backgroundColor: '#000',
  },
  liveIndicatorStream: {
    position: 'absolute',
    top: 10,
    left: 10,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 0, 0, 0.8)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  liveDotRecording: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#ffffff',
    marginRight: 8,
  },
  liveTextRecording: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  playButtonsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 20,
    gap: 30,
  },
  playButton: {
    alignItems: 'center',
  },
  playButtonSector: {
    alignItems: 'center',
  },
  playButtonText: {
    color: '#00d4ff',
    fontSize: 14,
    marginTop: 8,
  },
  playButtonTextSector: {
    color: '#ff6b35',
    fontSize: 14,
    marginTop: 8,
  },
  stopButton: {
    backgroundColor: 'rgba(255, 71, 87, 0.2)',
    borderRadius: 10,
  },
  cameraName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 12,
  },
  cameraLocation: {
    fontSize: 13,
    color: '#5a6a8a',
    marginTop: 5,
  },
  liveIndicator: {
    position: 'absolute',
    top: 15,
    right: 15,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  liveText: {
    color: '#ffffff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  controlsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 15,
    borderTopWidth: 1,
    borderTopColor: 'rgba(0, 212, 255, 0.1)',
  },
  controlButton: {
    alignItems: 'center',
    padding: 10,
  },
  controlText: {
    color: '#5a6a8a',
    fontSize: 10,
    marginTop: 5,
  },
  cameraListSection: {
    marginBottom: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  badge: {
    backgroundColor: '#00d4ff',
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 3,
    marginLeft: 10,
  },
  badgeText: {
    color: '#0a1628',
    fontSize: 12,
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
    padding: 40,
    backgroundColor: 'rgba(20, 35, 60, 0.4)',
    borderRadius: 15,
  },
  emptyText: {
    color: '#ffffff',
    fontSize: 16,
    marginTop: 15,
  },
  emptySubtext: {
    color: '#5a6a8a',
    fontSize: 12,
    marginTop: 8,
    textAlign: 'center',
  },
  cameraGrid: {
    gap: 12,
  },
  cameraCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    padding: 15,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.1)',
  },
  cameraCardSelected: {
    borderColor: '#00d4ff',
    backgroundColor: 'rgba(0, 212, 255, 0.1)',
  },
  cameraCardInactive: {
    opacity: 0.6,
  },
  cameraThumbnail: {
    width: 55,
    height: 55,
    backgroundColor: 'rgba(0, 212, 255, 0.1)',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  cameraInfo: {
    flex: 1,
  },
  cameraCardName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  cameraCardLocation: {
    fontSize: 12,
    color: '#5a6a8a',
    marginTop: 3,
  },
  cameraResolution: {
    fontSize: 11,
    color: '#00d4ff',
    marginTop: 2,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 10,
  },
  statusActive: {
    backgroundColor: 'rgba(46, 213, 115, 0.2)',
  },
  statusInactive: {
    backgroundColor: 'rgba(255, 71, 87, 0.2)',
  },
  statusBadgeText: {
    fontSize: 11,
    fontWeight: 'bold',
    color: '#2ed573',
  },
  statusTextInactive: {
    color: '#ff4757',
  },
  infoSection: {
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    padding: 20,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  infoText: {
    color: '#8a9ab0',
    fontSize: 12,
    marginLeft: 12,
    flex: 1,
  },
  // Estilos de Pantalla Completa
  fullscreenContainer: {
    flex: 1,
    backgroundColor: '#000000',
    justifyContent: 'center',
    alignItems: 'center',
  },
  fullscreenImage: {
    width: '100%',
    height: '100%',
    backgroundColor: '#000000',
  },
  fullscreenOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'space-between',
  },
  fullscreenHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: Platform.OS === 'ios' ? 50 : 20,
    paddingBottom: 15,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  fullscreenLiveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 0, 0, 0.9)',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 25,
  },
  fullscreenLiveDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#ffffff',
    marginRight: 8,
  },
  fullscreenLiveText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  fullscreenCameraName: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    flex: 1,
    textAlign: 'center',
    marginHorizontal: 15,
  },
  fullscreenCloseButton: {
    width: 45,
    height: 45,
    borderRadius: 25,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  fullscreenFooter: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 20,
    paddingBottom: Platform.OS === 'ios' ? 40 : 20,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
  },
  fullscreenControlButton: {
    alignItems: 'center',
    padding: 15,
    borderRadius: 15,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    minWidth: 80,
  },
  fullscreenStopButton: {
    backgroundColor: 'rgba(255, 71, 87, 0.2)',
  },
  fullscreenControlText: {
    color: '#ffffff',
    fontSize: 12,
    marginTop: 5,
    fontWeight: '500',
  },
});
