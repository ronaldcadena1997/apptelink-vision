import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Image,
  Dimensions,
  Modal,
  FlatList,
  ActivityIndicator,
  Alert,
  RefreshControl,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { API_ENDPOINTS, fetchAPI, API_BASE_URL } from '../config/api';

const { width } = Dimensions.get('window');
const imageWidth = width > 600 ? (width - 80) / 3 : (width - 60) / 2;

export default function IntrusosScreen() {
  const [imagenes, setImagenes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filtro, setFiltro] = useState('todos');
  const [modalVisible, setModalVisible] = useState(false);
  const [imagenSeleccionada, setImagenSeleccionada] = useState(null);
  const [imagenBase64, setImagenBase64] = useState(null);
  const [loadingImagen, setLoadingImagen] = useState(false);

  useEffect(() => {
    cargarImagenes();
  }, []);

  const cargarImagenes = async () => {
    setLoading(true);
    const response = await fetchAPI(API_ENDPOINTS.listarIntrusos);
    
    if (response.success) {
      setImagenes(response.imagenes || []);
    } else {
      console.error('Error cargando imágenes:', response.error);
    }
    setLoading(false);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await cargarImagenes();
    setRefreshing(false);
  };

  // Obtener líneas únicas para filtros
  const lineasUnicas = [...new Set(imagenes.map(img => img.linea))].sort();

  const filtros = [
    { id: 'todos', label: 'Todos', color: '#00d4ff' },
    ...lineasUnicas.map((linea, index) => ({
      id: linea,
      label: linea.replace('LINEA_', 'L').replace('LINEA ', 'L'),
      color: ['#ff4757', '#2ed573', '#ff6b35', '#00d4ff', '#ff00ff', '#ffff00', '#00ffff', '#ff8800'][index % 8],
    })),
  ];

  const imagenesFiltradas =
    filtro === 'todos'
      ? imagenes
      : imagenes.filter((img) => img.linea === filtro);

  const abrirDetalle = async (imagen) => {
    setImagenSeleccionada(imagen);
    setModalVisible(true);
    setLoadingImagen(true);
    
    // Cargar imagen en base64
    const response = await fetchAPI(API_ENDPOINTS.obtenerImagenBase64(imagen.archivo));
    if (response.success) {
      setImagenBase64(response.image);
    }
    setLoadingImagen(false);
  };

  const cerrarModal = () => {
    setModalVisible(false);
    setImagenSeleccionada(null);
    setImagenBase64(null);
  };

  const eliminarImagen = async (archivo) => {
    const confirmar = async () => {
      const response = await fetchAPI(API_ENDPOINTS.eliminarImagen(archivo), {
        method: 'DELETE',
      });
      
      if (response.success) {
        setImagenes(imagenes.filter(img => img.archivo !== archivo));
        cerrarModal();
        if (Platform.OS === 'web') {
          window.alert('✅ Imagen eliminada correctamente');
        } else {
          Alert.alert('Éxito', 'Imagen eliminada');
        }
      } else {
        if (Platform.OS === 'web') {
          window.alert('❌ Error: ' + (response.error || 'No se pudo eliminar'));
        } else {
          Alert.alert('Error', response.error);
        }
      }
    };

    if (Platform.OS === 'web') {
      // En web usar window.confirm
      const resultado = window.confirm('¿Estás seguro de eliminar esta imagen?\n\nEsta acción no se puede deshacer.');
      if (resultado) {
        await confirmar();
      }
    } else {
      // En móvil usar Alert
      Alert.alert(
        'Eliminar Imagen',
        '¿Estás seguro de eliminar esta imagen?',
        [
          { text: 'Cancelar', style: 'cancel' },
          {
            text: 'Eliminar',
            style: 'destructive',
            onPress: confirmar,
          },
        ]
      );
    }
  };

  const formatearTamano = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const renderImagen = ({ item }) => {
    const colorLinea = filtros.find(f => f.id === item.linea)?.color || '#00d4ff';

    return (
      <TouchableOpacity
        style={styles.imagenCard}
        onPress={() => abrirDetalle(item)}
        activeOpacity={0.8}
      >
        <View style={styles.imagenContainer}>
          <Image
            source={{ uri: `${API_BASE_URL}/api/intrusos/${item.archivo}` }}
            style={styles.thumbnail}
            resizeMode="cover"
          />
          <View style={[styles.lineaBadge, { backgroundColor: `${colorLinea}30` }]}>
            <Text style={[styles.lineaBadgeText, { color: colorLinea }]}>
              {item.linea.replace('LINEA_', 'L').replace('LINEA ', 'L')}
            </Text>
          </View>
        </View>

        <View style={styles.imagenInfo}>
          <View style={styles.imagenDetalle}>
            <Ionicons name="calendar" size={12} color="#5a6a8a" />
            <Text style={styles.imagenDetalleText}>{item.fecha}</Text>
          </View>
          <View style={styles.imagenDetalle}>
            <Ionicons name="time" size={12} color="#5a6a8a" />
            <Text style={styles.imagenDetalleText}>{item.hora}</Text>
          </View>
        </View>
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      {/* Header con estadísticas */}
      <View style={styles.statsHeader}>
        <View style={styles.statBox}>
          <Ionicons name="images" size={22} color="#00d4ff" />
          <Text style={styles.statNumber}>{imagenes.length}</Text>
          <Text style={styles.statLabel}>Total</Text>
        </View>
        <View style={styles.statBox}>
          <Ionicons name="today" size={22} color="#2ed573" />
          <Text style={[styles.statNumber, { color: '#2ed573' }]}>
            {imagenes.filter(img => img.fecha === new Date().toISOString().split('T')[0].split('-').reverse().join('-')).length}
          </Text>
          <Text style={styles.statLabel}>Hoy</Text>
        </View>
        <View style={styles.statBox}>
          <Ionicons name="folder" size={22} color="#ff6b35" />
          <Text style={[styles.statNumber, { color: '#ff6b35' }]}>
            {lineasUnicas.length}
          </Text>
          <Text style={styles.statLabel}>Líneas</Text>
        </View>
      </View>

      {/* Filtros */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.filtrosContainer}
        contentContainerStyle={styles.filtrosContent}
      >
        {filtros.map((f) => (
          <TouchableOpacity
            key={f.id}
            style={[
              styles.filtroButton,
              filtro === f.id && { backgroundColor: `${f.color}20`, borderColor: f.color },
            ]}
            onPress={() => setFiltro(f.id)}
          >
            <Text
              style={[styles.filtroText, filtro === f.id && { color: f.color }]}
            >
              {f.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Lista de imágenes */}
      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#00d4ff" />
          <Text style={styles.loadingText}>Cargando imágenes...</Text>
        </View>
      ) : (
        <FlatList
          data={imagenesFiltradas}
          renderItem={renderImagen}
          keyExtractor={(item) => item.id.toString()}
          numColumns={width > 600 ? 3 : 2}
          contentContainerStyle={styles.listaContent}
          columnWrapperStyle={styles.listaRow}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#00d4ff" />
          }
          ListEmptyComponent={
            <View style={styles.emptyState}>
              <Ionicons name="shield-checkmark" size={60} color="#3a4a6a" />
              <Text style={styles.emptyText}>No hay imágenes de intrusos</Text>
              <Text style={styles.emptySubtext}>
                Las capturas aparecerán aquí cuando se detecten intrusiones
              </Text>
            </View>
          }
        />
      )}

      {/* Modal de detalle */}
      <Modal
        visible={modalVisible}
        transparent
        animationType="fade"
        onRequestClose={cerrarModal}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            {imagenSeleccionada && (
              <>
                <View style={styles.modalHeader}>
                  <Text style={styles.modalTitle}>Detalle de Alerta</Text>
                  <TouchableOpacity onPress={cerrarModal}>
                    <Ionicons name="close" size={24} color="#ffffff" />
                  </TouchableOpacity>
                </View>

                {/* Imagen */}
                <View style={styles.modalImageContainer}>
                  {loadingImagen ? (
                    <View style={styles.modalImagePlaceholder}>
                      <ActivityIndicator size="large" color="#00d4ff" />
                    </View>
                  ) : imagenBase64 ? (
                    <Image
                      source={{ uri: imagenBase64 }}
                      style={styles.modalImage}
                      resizeMode="contain"
                    />
                  ) : (
                    <View style={styles.modalImagePlaceholder}>
                      <Ionicons name="image" size={60} color="#3a4a6a" />
                    </View>
                  )}
                </View>

                {/* Información */}
                <View style={styles.modalInfo}>
                  <View style={styles.modalInfoRow}>
                    <Ionicons name="alert-circle" size={18} color="#ff4757" />
                    <Text style={styles.modalInfoLabel}>Línea:</Text>
                    <Text style={styles.modalInfoValue}>
                      {imagenSeleccionada.linea}
                    </Text>
                  </View>
                  <View style={styles.modalInfoRow}>
                    <Ionicons name="calendar" size={18} color="#00d4ff" />
                    <Text style={styles.modalInfoLabel}>Fecha:</Text>
                    <Text style={styles.modalInfoValue}>
                      {imagenSeleccionada.fecha}
                    </Text>
                  </View>
                  <View style={styles.modalInfoRow}>
                    <Ionicons name="time" size={18} color="#2ed573" />
                    <Text style={styles.modalInfoLabel}>Hora:</Text>
                    <Text style={styles.modalInfoValue}>
                      {imagenSeleccionada.hora}
                    </Text>
                  </View>
                  <View style={styles.modalInfoRow}>
                    <Ionicons name="document" size={18} color="#ff6b35" />
                    <Text style={styles.modalInfoLabel}>Tamaño:</Text>
                    <Text style={styles.modalInfoValue}>
                      {formatearTamano(imagenSeleccionada.tamano)}
                    </Text>
                  </View>
                  <View style={styles.modalInfoRow}>
                    <Ionicons name="folder" size={18} color="#5a6a8a" />
                    <Text style={styles.modalInfoLabel}>Archivo:</Text>
                    <Text style={[styles.modalInfoValue, { fontSize: 10 }]} numberOfLines={1}>
                      {imagenSeleccionada.archivo}
                    </Text>
                  </View>
                </View>

                {/* Acciones */}
                <TouchableOpacity
                  style={styles.deleteImageButton}
                  onPress={() => eliminarImagen(imagenSeleccionada.archivo)}
                >
                  <Ionicons name="trash" size={20} color="#ff4757" />
                  <Text style={styles.deleteImageButtonText}>Eliminar Imagen</Text>
                </TouchableOpacity>
              </>
            )}
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
  statsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 20,
    paddingHorizontal: 15,
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 212, 255, 0.1)',
  },
  statBox: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#00d4ff',
    marginTop: 5,
  },
  statLabel: {
    fontSize: 11,
    color: '#5a6a8a',
    marginTop: 3,
  },
  filtrosContainer: {
    maxHeight: 60,
  },
  filtrosContent: {
    paddingHorizontal: 15,
    paddingVertical: 15,
    gap: 10,
  },
  filtroButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#3a4a6a',
    marginRight: 10,
  },
  filtroText: {
    color: '#5a6a8a',
    fontSize: 12,
    fontWeight: '500',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#5a6a8a',
    marginTop: 15,
  },
  listaContent: {
    padding: 15,
    paddingBottom: 30,
  },
  listaRow: {
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  imagenCard: {
    width: imageWidth,
    backgroundColor: 'rgba(20, 35, 60, 0.8)',
    borderRadius: 15,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.15)',
  },
  imagenContainer: {
    position: 'relative',
  },
  thumbnail: {
    width: '100%',
    height: 100,
    backgroundColor: '#0d1f38',
  },
  lineaBadge: {
    position: 'absolute',
    top: 8,
    right: 8,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 10,
  },
  lineaBadgeText: {
    fontSize: 10,
    fontWeight: 'bold',
  },
  imagenInfo: {
    padding: 10,
  },
  imagenDetalle: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  imagenDetalleText: {
    fontSize: 11,
    color: '#5a6a8a',
    marginLeft: 5,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
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
    paddingHorizontal: 30,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    width: '100%',
    maxWidth: 500,
    backgroundColor: '#14233c',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.2)',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  modalImageContainer: {
    marginBottom: 20,
    borderRadius: 12,
    overflow: 'hidden',
  },
  modalImage: {
    width: '100%',
    height: 250,
    backgroundColor: '#0d1f38',
  },
  modalImagePlaceholder: {
    width: '100%',
    height: 200,
    backgroundColor: '#0d1f38',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 12,
  },
  modalInfo: {
    marginBottom: 20,
  },
  modalInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  modalInfoLabel: {
    color: '#5a6a8a',
    fontSize: 13,
    marginLeft: 10,
    marginRight: 8,
  },
  modalInfoValue: {
    color: '#ffffff',
    fontSize: 13,
    fontWeight: '500',
    flex: 1,
  },
  deleteImageButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 10,
    backgroundColor: 'rgba(255, 71, 87, 0.15)',
    borderWidth: 1,
    borderColor: '#ff4757',
    gap: 8,
  },
  deleteImageButtonText: {
    color: '#ff4757',
    fontSize: 14,
    fontWeight: 'bold',
  },
});
