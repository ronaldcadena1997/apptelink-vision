import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Switch,
  Alert,
  ActivityIndicator,
  RefreshControl,
  Platform,
  Image,
  Modal,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { API_ENDPOINTS, fetchAPI, API_BASE_URL } from '../config/api';

const { width: screenWidth } = Dimensions.get('window');

const COLORES = [
  { nombre: 'Amarillo', hex: '#FFFF00', index: 0 },
  { nombre: 'Naranja', hex: '#FFA500', index: 1 },
  { nombre: 'Magenta', hex: '#FF00FF', index: 2 },
  { nombre: 'Cyan', hex: '#00FFFF', index: 3 },
  { nombre: 'Verde', hex: '#00FF00', index: 4 },
  { nombre: 'Rojo', hex: '#FF0000', index: 5 },
  { nombre: 'Azul', hex: '#0000FF', index: 6 },
];

export default function ConfiguracionScreen() {
  const [cercas, setCercas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [serverOnline, setServerOnline] = useState(false);
  
  // Estado del configurador visual
  const [modalVisible, setModalVisible] = useState(false);
  const [camaras, setCamaras] = useState([]);
  const [camaraSeleccionada, setCamaraSeleccionada] = useState(null);
  const [snapshotBase64, setSnapshotBase64] = useState(null);
  const [loadingSnapshot, setLoadingSnapshot] = useState(false);
  const [puntoTemp, setPuntoTemp] = useState(null);
  const [lineasTemp, setLineasTemp] = useState([]);
  const [colorActual, setColorActual] = useState(0);
  const [contadorLineas, setContadorLineas] = useState(1);
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  const [naturalSize, setNaturalSize] = useState({ width: 1920, height: 1080 }); // Tamaño natural de la imagen
  
  const imageRef = useRef(null);

  useEffect(() => {
    verificarServidor();
    cargarCamaras();
  }, []);

  // Cargar cercas cuando cambia la cámara seleccionada
  useEffect(() => {
    if (camaraSeleccionada) {
      cargarCercas(camaraSeleccionada);
    }
  }, [camaraSeleccionada]);

  const verificarServidor = async () => {
    const response = await fetchAPI(API_ENDPOINTS.status);
    setServerOnline(response.status === 'online');
  };

  const cargarCercas = async (ip) => {
    if (!ip) return;
    setLoading(true);
    const response = await fetchAPI(API_ENDPOINTS.obtenerCercas(ip));
    
    if (response.success) {
      setCercas(response.cercas || []);
      setContadorLineas((response.cercas?.length || 0) + 1);
    }
    setLoading(false);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await verificarServidor();
    await cargarCamaras();
    if (camaraSeleccionada) {
      await cargarCercas(camaraSeleccionada);
    }
    setRefreshing(false);
  };

  const cargarCamaras = async () => {
    const response = await fetchAPI(API_ENDPOINTS.listarCamaras);
    if (response.success && response.camaras) {
      setCamaras(response.camaras);
      if (response.camaras.length > 0 && !camaraSeleccionada) {
        setCamaraSeleccionada(response.camaras[0].ip);
      }
    }
  };

  const abrirConfiguradorVisual = async () => {
    setModalVisible(true);
    // Cargar cercas existentes de la cámara seleccionada
    if (camaraSeleccionada) {
      await cargarCercas(camaraSeleccionada);
    }
    setLineasTemp([...cercas.map(c => ({
      x1: c.x1,
      y1: c.y1,
      x2: c.x2,
      y2: c.y2,
      nombre: c.nombre,
      color_index: c.color_index || 0,
    }))]);
  };

  const capturarSnapshot = async () => {
    if (!camaraSeleccionada) {
      showAlert('Error', 'Selecciona una cámara primero');
      return;
    }
    
    setLoadingSnapshot(true);
    const response = await fetchAPI(API_ENDPOINTS.snapshotCamara(camaraSeleccionada));
    
    if (response.success && response.image) {
      setSnapshotBase64(response.image);
      
      // Obtener dimensiones naturales de la imagen
      if (Platform.OS === 'web') {
        const img = new window.Image();
        img.onload = () => {
          setNaturalSize({ width: img.naturalWidth, height: img.naturalHeight });
        };
        img.src = response.image;
      } else {
        Image.getSize(response.image, (width, height) => {
          setNaturalSize({ width, height });
        });
      }
    } else {
      showAlert('Error', 'No se pudo capturar la imagen de la cámara');
    }
    setLoadingSnapshot(false);
  };

  const showAlert = (title, message) => {
    if (Platform.OS === 'web') {
      window.alert(`${title}\n\n${message}`);
    } else {
      Alert.alert(title, message);
    }
  };

  const handleImageClick = (event) => {
    if (!snapshotBase64 || !containerSize.width) return;
    
    // Obtener coordenadas del click relativas al contenedor
    let clickX, clickY;
    
    if (Platform.OS === 'web') {
      const rect = event.target.getBoundingClientRect();
      clickX = event.clientX - rect.left;
      clickY = event.clientY - rect.top;
    } else {
      clickX = event.nativeEvent.locationX;
      clickY = event.nativeEvent.locationY;
    }
    
    // Calcular cómo se escala la imagen con "contain"
    const containerAspect = containerSize.width / containerSize.height;
    const imageAspect = naturalSize.width / naturalSize.height;
    
    let displayWidth, displayHeight, offsetX, offsetY;
    
    if (imageAspect > containerAspect) {
      // Imagen más ancha - se ajusta al ancho del contenedor
      displayWidth = containerSize.width;
      displayHeight = containerSize.width / imageAspect;
      offsetX = 0;
      offsetY = (containerSize.height - displayHeight) / 2;
    } else {
      // Imagen más alta - se ajusta a la altura del contenedor
      displayHeight = containerSize.height;
      displayWidth = containerSize.height * imageAspect;
      offsetX = (containerSize.width - displayWidth) / 2;
      offsetY = 0;
    }
    
    // Ajustar coordenadas del click restando el offset
    const imgX = clickX - offsetX;
    const imgY = clickY - offsetY;
    
    // Verificar que el click está dentro de la imagen
    if (imgX < 0 || imgY < 0 || imgX > displayWidth || imgY > displayHeight) {
      return; // Click fuera de la imagen
    }
    
    // Convertir a porcentajes de la imagen real
    const xPct = Math.round((imgX / displayWidth) * 1000) / 10;
    const yPct = Math.round((imgY / displayHeight) * 1000) / 10;
    
    // Limitar a 0-100
    const xFinal = Math.max(0, Math.min(100, xPct));
    const yFinal = Math.max(0, Math.min(100, yPct));
    
    if (puntoTemp === null) {
      // Primer punto
      setPuntoTemp({ x: xFinal, y: yFinal });
    } else {
      // Segundo punto - crear línea
      const nuevaLinea = {
        x1: puntoTemp.x,
        y1: puntoTemp.y,
        x2: xFinal,
        y2: yFinal,
        nombre: `LINEA ${contadorLineas}`,
        color_index: colorActual,
      };
      
      setLineasTemp([...lineasTemp, nuevaLinea]);
      setContadorLineas(contadorLineas + 1);
      setColorActual((colorActual + 1) % COLORES.length);
      setPuntoTemp(null);
    }
    
    // Actualizar el tamaño de imagen mostrado para el renderizado de líneas
    setImageSize({ width: displayWidth, height: displayHeight });
  };

  const borrarUltimaLinea = () => {
    if (lineasTemp.length > 0) {
      const nuevasLineas = [...lineasTemp];
      nuevasLineas.pop();
      setLineasTemp(nuevasLineas);
      setContadorLineas(Math.max(1, contadorLineas - 1));
    }
    setPuntoTemp(null);
  };

  const borrarTodasLineas = () => {
    if (Platform.OS === 'web') {
      if (window.confirm('¿Borrar todas las líneas?')) {
        setLineasTemp([]);
        setContadorLineas(1);
        setPuntoTemp(null);
      }
    } else {
      Alert.alert('Confirmar', '¿Borrar todas las líneas?', [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Borrar', style: 'destructive', onPress: () => {
          setLineasTemp([]);
          setContadorLineas(1);
          setPuntoTemp(null);
        }},
      ]);
    }
  };

  const guardarConfiguracion = async () => {
    if (!camaraSeleccionada) {
      showAlert('Error', 'Selecciona una cámara primero');
      return;
    }
    
    const response = await fetchAPI(API_ENDPOINTS.guardarCercas(camaraSeleccionada), {
      method: 'POST',
      body: JSON.stringify({ lineas: lineasTemp }),
    });

    if (response.success) {
      showAlert('Éxito', `✅ Configuración guardada para cámara ${camaraSeleccionada}`);
      await cargarCercas(camaraSeleccionada);
      setModalVisible(false);
    } else {
      showAlert('Error', response.error || 'No se pudo guardar');
    }
  };

  const toggleCerca = (nombre) => {
    setCercas(cercas.map(cerca => 
      cerca.nombre === nombre 
        ? { ...cerca, activa: !cerca.activa }
        : cerca
    ));
  };

  const eliminarCerca = async (nombre) => {
    if (!camaraSeleccionada) {
      showAlert('Error', 'No hay cámara seleccionada');
      return;
    }
    
    const ejecutarEliminar = async () => {
      const response = await fetchAPI(API_ENDPOINTS.eliminarCerca(camaraSeleccionada, nombre), {
        method: 'DELETE',
      });
      
      if (response.success) {
        setCercas(cercas.filter(c => c.nombre !== nombre));
        showAlert('Éxito', '✅ ' + response.message);
      } else {
        showAlert('Error', '❌ ' + response.error);
      }
    };

    if (Platform.OS === 'web') {
      if (window.confirm(`¿Eliminar "${nombre}" de cámara ${camaraSeleccionada}?`)) {
        await ejecutarEliminar();
      }
    } else {
      Alert.alert('Eliminar', `¿Eliminar "${nombre}"?`, [
        { text: 'Cancelar', style: 'cancel' },
        { text: 'Eliminar', style: 'destructive', onPress: ejecutarEliminar },
      ]);
    }
  };

  const onContainerLayout = (event) => {
    const { width, height } = event.nativeEvent.layout;
    setContainerSize({ width, height });
    
    // Calcular tamaño de imagen mostrada
    const containerAspect = width / height;
    const imageAspect = naturalSize.width / naturalSize.height;
    
    let displayWidth, displayHeight;
    
    if (imageAspect > containerAspect) {
      displayWidth = width;
      displayHeight = width / imageAspect;
    } else {
      displayHeight = height;
      displayWidth = height * imageAspect;
    }
    
    setImageSize({ width: displayWidth, height: displayHeight });
  };

  const renderLineasSVG = () => {
    if (!imageSize.width || !containerSize.width) return null;
    
    // Calcular offset para centrar las líneas sobre la imagen
    const containerAspect = containerSize.width / containerSize.height;
    const imageAspect = naturalSize.width / naturalSize.height;
    
    let offsetX = 0, offsetY = 0;
    
    if (imageAspect > containerAspect) {
      // Imagen más ancha - centrada verticalmente
      offsetY = (containerSize.height - imageSize.height) / 2;
    } else {
      // Imagen más alta - centrada horizontalmente
      offsetX = (containerSize.width - imageSize.width) / 2;
    }
    
    return (
      <View style={StyleSheet.absoluteFill} pointerEvents="none">
        {/* Dibujar líneas */}
        {lineasTemp.map((linea, index) => {
          const x1 = offsetX + (linea.x1 / 100) * imageSize.width;
          const y1 = offsetY + (linea.y1 / 100) * imageSize.height;
          const x2 = offsetX + (linea.x2 / 100) * imageSize.width;
          const y2 = offsetY + (linea.y2 / 100) * imageSize.height;
          const color = COLORES[linea.color_index]?.hex || '#00FFFF';
          
          // Calcular ángulo y longitud de la línea
          const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
          const angle = Math.atan2(y2 - y1, x2 - x1) * (180 / Math.PI);
          
          return (
            <View key={index}>
              {/* Línea */}
              <View
                style={{
                  position: 'absolute',
                  left: x1,
                  top: y1,
                  width: length,
                  height: 4,
                  backgroundColor: color,
                  transform: [{ rotate: `${angle}deg` }],
                  transformOrigin: 'left center',
                  shadowColor: '#000',
                  shadowOffset: { width: 0, height: 2 },
                  shadowOpacity: 0.5,
                  shadowRadius: 3,
                }}
              />
              {/* Punto inicio */}
              <View
                style={{
                  position: 'absolute',
                  left: x1 - 6,
                  top: y1 - 6,
                  width: 12,
                  height: 12,
                  borderRadius: 6,
                  backgroundColor: color,
                  borderWidth: 2,
                  borderColor: '#000',
                }}
              />
              {/* Punto fin */}
              <View
                style={{
                  position: 'absolute',
                  left: x2 - 6,
                  top: y2 - 6,
                  width: 12,
                  height: 12,
                  borderRadius: 6,
                  backgroundColor: color,
                  borderWidth: 2,
                  borderColor: '#000',
                }}
              />
              {/* Etiqueta */}
              <View
                style={{
                  position: 'absolute',
                  left: (x1 + x2) / 2 - 40,
                  top: (y1 + y2) / 2 - 12,
                  backgroundColor: 'rgba(0,0,0,0.8)',
                  paddingHorizontal: 8,
                  paddingVertical: 3,
                  borderRadius: 4,
                }}
              >
                <Text style={{ color: color, fontSize: 11, fontWeight: 'bold' }}>
                  {linea.nombre}
                </Text>
              </View>
            </View>
          );
        })}
        
        {/* Punto temporal */}
        {puntoTemp && (() => {
          const containerAspect = containerSize.width / containerSize.height;
          const imageAspect = naturalSize.width / naturalSize.height;
          let pOffsetX = 0, pOffsetY = 0;
          if (imageAspect > containerAspect) {
            pOffsetY = (containerSize.height - imageSize.height) / 2;
          } else {
            pOffsetX = (containerSize.width - imageSize.width) / 2;
          }
          return (
            <View
              style={{
                position: 'absolute',
                left: pOffsetX + (puntoTemp.x / 100) * imageSize.width - 8,
                top: pOffsetY + (puntoTemp.y / 100) * imageSize.height - 8,
                width: 16,
                height: 16,
                borderRadius: 8,
                backgroundColor: COLORES[colorActual].hex,
                borderWidth: 3,
                borderColor: '#fff',
              }}
            />
          );
        })()}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#00d4ff" />
        }
      >
        {/* Estado del servidor */}
        <View style={[styles.serverStatus, serverOnline ? styles.serverOnline : styles.serverOffline]}>
          <Ionicons 
            name={serverOnline ? "cloud-done" : "cloud-offline"} 
            size={20} 
            color={serverOnline ? "#2ed573" : "#ff4757"} 
          />
          <Text style={[styles.serverStatusText, { color: serverOnline ? "#2ed573" : "#ff4757" }]}>
            Servidor {serverOnline ? "Conectado" : "Desconectado"}
          </Text>
        </View>

        {/* Header */}
        <View style={styles.headerCard}>
          <View style={styles.headerIconContainer}>
            <Ionicons name="shield-checkmark" size={40} color="#00d4ff" />
          </View>
          <View style={styles.headerInfo}>
            <Text style={styles.headerTitle}>Configuración de Cercas</Text>
            <Text style={styles.headerSubtitle}>
              Cada cámara tiene su propia configuración
            </Text>
          </View>
        </View>

        {/* Selector de Cámara */}
        <View style={styles.cameraSelectorMain}>
          <Text style={styles.cameraSelectorLabel}>📷 Seleccionar Cámara:</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.cameraScrollMain}>
            {camaras.length === 0 ? (
              <Text style={styles.noCamerasText}>No hay cámaras detectadas</Text>
            ) : (
              camaras.map((cam, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.cameraChip,
                    camaraSeleccionada === cam.ip && styles.cameraChipSelected,
                  ]}
                  onPress={() => setCamaraSeleccionada(cam.ip)}
                >
                  <Ionicons 
                    name="videocam" 
                    size={16} 
                    color={camaraSeleccionada === cam.ip ? '#0a1628' : '#00d4ff'} 
                  />
                  <Text style={[
                    styles.cameraChipText,
                    camaraSeleccionada === cam.ip && styles.cameraChipTextSelected,
                  ]}>
                    {cam.ip}
                  </Text>
                </TouchableOpacity>
              ))
            )}
          </ScrollView>
        </View>

        {/* Botón para abrir configurador visual */}
        <TouchableOpacity
          style={[styles.openConfigButton, !camaraSeleccionada && styles.buttonDisabled]}
          onPress={abrirConfiguradorVisual}
          disabled={!camaraSeleccionada}
        >
          <Ionicons name="create" size={22} color="#0a1628" />
          <Text style={styles.openConfigButtonText}>
            {camaraSeleccionada 
              ? `CONFIGURAR CERCAS - ${camaraSeleccionada}` 
              : 'SELECCIONA UNA CÁMARA'}
          </Text>
        </TouchableOpacity>

        {/* Lista de cercas */}
        <View style={styles.cercasSection}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Cercas Configuradas</Text>
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{cercas.length}</Text>
            </View>
          </View>

          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#00d4ff" />
              <Text style={styles.loadingText}>Cargando cercas...</Text>
            </View>
          ) : cercas.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="remove-circle-outline" size={50} color="#3a4a6a" />
              <Text style={styles.emptyText}>No hay cercas configuradas</Text>
              <Text style={styles.emptySubtext}>
                Usa el configurador visual para crear líneas de detección
              </Text>
            </View>
          ) : (
            cercas.map((cerca, index) => (
              <View key={index} style={styles.cercaCard}>
                <View style={styles.cercaHeader}>
                  <View style={styles.cercaNameContainer}>
                    <View
                      style={[
                        styles.cercaColorIndicator,
                        { backgroundColor: COLORES[cerca.color_index]?.hex || '#00d4ff' },
                      ]}
                    />
                    <Text style={styles.cercaName}>{cerca.nombre}</Text>
                  </View>
                  <Switch
                    value={cerca.activa !== false}
                    onValueChange={() => toggleCerca(cerca.nombre)}
                    trackColor={{ false: '#3a4a6a', true: 'rgba(46, 213, 115, 0.4)' }}
                    thumbColor={cerca.activa !== false ? '#2ed573' : '#5a6a8a'}
                  />
                </View>

                <View style={styles.cercaDetails}>
                  <View style={styles.detailRow}>
                    <Ionicons name="color-palette" size={14} color="#5a6a8a" />
                    <Text style={styles.detailLabel}>Color:</Text>
                    <Text style={[styles.detailValue, { color: COLORES[cerca.color_index]?.hex || '#fff' }]}>
                      {COLORES[cerca.color_index]?.nombre || 'Cyan'}
                    </Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Ionicons name="locate" size={14} color="#5a6a8a" />
                    <Text style={styles.detailLabel}>Inicio:</Text>
                    <Text style={styles.detailValue}>({cerca.x1}%, {cerca.y1}%)</Text>
                  </View>
                  <View style={styles.detailRow}>
                    <Ionicons name="locate" size={14} color="#5a6a8a" />
                    <Text style={styles.detailLabel}>Fin:</Text>
                    <Text style={styles.detailValue}>({cerca.x2}%, {cerca.y2}%)</Text>
                  </View>
                </View>

                <TouchableOpacity
                  style={styles.deleteButton}
                  onPress={() => eliminarCerca(cerca.nombre)}
                >
                  <Ionicons name="trash-outline" size={18} color="#ff4757" />
                  <Text style={styles.deleteButtonText}>Eliminar</Text>
                </TouchableOpacity>
              </View>
            ))
          )}
        </View>

        {/* Instrucciones */}
        <View style={styles.instructionsCard}>
          <Text style={styles.instructionsTitle}>📋 Instrucciones</Text>
          <View style={styles.instruction}>
            <Text style={styles.instructionBullet}>1.</Text>
            <Text style={styles.instructionText}>Abre el configurador visual</Text>
          </View>
          <View style={styles.instruction}>
            <Text style={styles.instructionBullet}>2.</Text>
            <Text style={styles.instructionText}>Selecciona una cámara y captura imagen</Text>
          </View>
          <View style={styles.instruction}>
            <Text style={styles.instructionBullet}>3.</Text>
            <Text style={styles.instructionText}>Haz clic en 2 puntos para crear una línea</Text>
          </View>
          <View style={styles.instruction}>
            <Text style={styles.instructionBullet}>4.</Text>
            <Text style={styles.instructionText}>Guarda la configuración</Text>
          </View>
        </View>
      </ScrollView>

      {/* Modal del configurador visual */}
      <Modal
        visible={modalVisible}
        animationType="slide"
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          {/* Header del modal */}
          <View style={styles.modalHeader}>
            <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
              <Ionicons name="close" size={28} color="#fff" />
            </TouchableOpacity>
            <Text style={styles.modalTitle}>Configurador de Cercas</Text>
            <TouchableOpacity onPress={guardarConfiguracion} style={styles.saveModalButton}>
              <Ionicons name="save" size={24} color="#0a1628" />
            </TouchableOpacity>
          </View>

          {/* Selector de cámara */}
          <View style={styles.cameraSelector}>
            <Text style={styles.selectorLabel}>Seleccionar Cámara:</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {camaras.map((cam, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.cameraOption,
                    camaraSeleccionada === cam.ip && styles.cameraOptionSelected,
                  ]}
                  onPress={() => {
                    setCamaraSeleccionada(cam.ip);
                    setSnapshotBase64(null);
                  }}
                >
                  <Text style={styles.cameraOptionText}>{cam.ip}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
            <TouchableOpacity style={styles.captureButton} onPress={capturarSnapshot}>
              {loadingSnapshot ? (
                <ActivityIndicator color="#0a1628" size="small" />
              ) : (
                <>
                  <Ionicons name="camera" size={20} color="#0a1628" />
                  <Text style={styles.captureButtonText}>Capturar</Text>
                </>
              )}
            </TouchableOpacity>
          </View>

          {/* Área de la imagen */}
          <View style={styles.imageContainer}>
            {snapshotBase64 ? (
              <TouchableOpacity
                activeOpacity={1}
                onPress={handleImageClick}
                onLayout={onContainerLayout}
                style={styles.imageTouchable}
              >
                <Image
                  ref={imageRef}
                  source={{ uri: snapshotBase64 }}
                  style={styles.cameraImage}
                  resizeMode="contain"
                />
                {renderLineasSVG()}
              </TouchableOpacity>
            ) : (
              <View style={styles.noImageContainer}>
                <Ionicons name="camera-outline" size={80} color="#3a4a6a" />
                <Text style={styles.noImageText}>Selecciona una cámara y presiona "Capturar"</Text>
              </View>
            )}
          </View>

          {/* Panel de control */}
          <View style={styles.controlPanel}>
            {/* Información */}
            <View style={styles.infoRow}>
              <Text style={styles.infoText}>
                Líneas: {lineasTemp.length} | Color actual: 
              </Text>
              <View style={[styles.colorPreview, { backgroundColor: COLORES[colorActual].hex }]} />
              <Text style={[styles.infoText, { color: COLORES[colorActual].hex }]}>
                {COLORES[colorActual].nombre}
              </Text>
            </View>

            {puntoTemp && (
              <Text style={styles.helpText}>
                ✓ Primer punto en ({puntoTemp.x}%, {puntoTemp.y}%) - Haz clic en el segundo punto
              </Text>
            )}

            {/* Botones de acción */}
            <View style={styles.actionButtons}>
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => setColorActual((colorActual + 1) % COLORES.length)}
              >
                <Ionicons name="color-palette" size={20} color="#fff" />
                <Text style={styles.actionButtonText}>Color</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.actionButton, styles.actionButtonWarning]}
                onPress={borrarUltimaLinea}
              >
                <Ionicons name="arrow-undo" size={20} color="#fff" />
                <Text style={styles.actionButtonText}>Deshacer</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.actionButton, styles.actionButtonDanger]}
                onPress={borrarTodasLineas}
              >
                <Ionicons name="trash" size={20} color="#fff" />
                <Text style={styles.actionButtonText}>Borrar Todo</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.actionButton, styles.actionButtonSuccess]}
                onPress={guardarConfiguracion}
              >
                <Ionicons name="checkmark" size={20} color="#fff" />
                <Text style={styles.actionButtonText}>Guardar</Text>
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
  serverStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 10,
    borderRadius: 10,
    marginBottom: 15,
  },
  serverOnline: {
    backgroundColor: 'rgba(46, 213, 115, 0.15)',
  },
  serverOffline: {
    backgroundColor: 'rgba(255, 71, 87, 0.15)',
  },
  serverStatusText: {
    marginLeft: 8,
    fontSize: 13,
    fontWeight: '600',
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
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerSubtitle: {
    fontSize: 13,
    color: '#5a6a8a',
    marginTop: 4,
  },
  cameraSelectorMain: {
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.2)',
  },
  cameraSelectorLabel: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 12,
  },
  cameraScrollMain: {
    flexDirection: 'row',
  },
  noCamerasText: {
    color: '#5a6a8a',
    fontSize: 13,
    fontStyle: 'italic',
  },
  cameraChip: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 212, 255, 0.1)',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.3)',
    gap: 8,
  },
  cameraChipSelected: {
    backgroundColor: '#00d4ff',
    borderColor: '#00d4ff',
  },
  cameraChipText: {
    color: '#00d4ff',
    fontSize: 13,
    fontWeight: '600',
  },
  cameraChipTextSelected: {
    color: '#0a1628',
  },
  buttonDisabled: {
    backgroundColor: '#3a4a6a',
    opacity: 0.6,
  },
  openConfigButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ff6b35',
    borderRadius: 12,
    height: 55,
    marginBottom: 20,
    gap: 10,
  },
  openConfigButtonText: {
    color: '#0a1628',
    fontSize: 14,
    fontWeight: 'bold',
  },
  cercasSection: {
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
  cercaCard: {
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    padding: 18,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.1)',
  },
  cercaHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  cercaNameContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  cercaColorIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 10,
  },
  cercaName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  cercaDetails: {
    marginLeft: 22,
    gap: 6,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  detailLabel: {
    fontSize: 12,
    color: '#5a6a8a',
    marginLeft: 8,
    marginRight: 8,
  },
  detailValue: {
    fontSize: 12,
    color: '#8a9ab0',
  },
  deleteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 15,
    padding: 10,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 71, 87, 0.15)',
  },
  deleteButtonText: {
    color: '#ff4757',
    fontSize: 13,
    marginLeft: 6,
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
    marginBottom: 15,
  },
  instruction: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  instructionBullet: {
    color: '#00d4ff',
    fontSize: 14,
    fontWeight: 'bold',
    marginRight: 10,
    width: 20,
  },
  instructionText: {
    color: '#8a9ab0',
    fontSize: 13,
    flex: 1,
  },

  // Modal styles
  modalContainer: {
    flex: 1,
    backgroundColor: '#0a1628',
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 15,
    backgroundColor: 'rgba(20, 35, 60, 0.95)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 212, 255, 0.2)',
  },
  closeButton: {
    padding: 5,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  saveModalButton: {
    backgroundColor: '#2ed573',
    padding: 8,
    borderRadius: 8,
  },
  cameraSelector: {
    padding: 15,
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 212, 255, 0.1)',
  },
  selectorLabel: {
    color: '#8a9ab0',
    fontSize: 12,
    marginBottom: 8,
  },
  cameraOption: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    backgroundColor: 'rgba(0, 212, 255, 0.1)',
    borderRadius: 8,
    marginRight: 10,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  cameraOptionSelected: {
    backgroundColor: 'rgba(0, 212, 255, 0.3)',
    borderColor: '#00d4ff',
  },
  cameraOptionText: {
    color: '#ffffff',
    fontSize: 13,
  },
  captureButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#00d4ff',
    borderRadius: 8,
    paddingVertical: 10,
    marginTop: 10,
    gap: 8,
  },
  captureButtonText: {
    color: '#0a1628',
    fontWeight: 'bold',
    fontSize: 14,
  },
  imageContainer: {
    flex: 1,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageTouchable: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cameraImage: {
    width: '100%',
    height: '100%',
  },
  noImageContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  noImageText: {
    color: '#5a6a8a',
    fontSize: 14,
    marginTop: 15,
    textAlign: 'center',
  },
  controlPanel: {
    padding: 15,
    backgroundColor: 'rgba(20, 35, 60, 0.95)',
    borderTopWidth: 1,
    borderTopColor: 'rgba(0, 212, 255, 0.2)',
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  infoText: {
    color: '#ffffff',
    fontSize: 13,
  },
  colorPreview: {
    width: 16,
    height: 16,
    borderRadius: 4,
    marginHorizontal: 8,
    borderWidth: 1,
    borderColor: '#fff',
  },
  helpText: {
    color: '#2ed573',
    fontSize: 12,
    marginBottom: 10,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(0, 212, 255, 0.2)',
    borderRadius: 8,
    paddingVertical: 12,
    gap: 6,
  },
  actionButtonWarning: {
    backgroundColor: 'rgba(255, 165, 0, 0.3)',
  },
  actionButtonDanger: {
    backgroundColor: 'rgba(255, 71, 87, 0.3)',
  },
  actionButtonSuccess: {
    backgroundColor: 'rgba(46, 213, 115, 0.3)',
  },
  actionButtonText: {
    color: '#ffffff',
    fontSize: 11,
    fontWeight: '600',
  },
});
