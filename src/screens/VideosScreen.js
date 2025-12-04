import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
  Modal,
  FlatList,
  ActivityIndicator,
  Alert,
  RefreshControl,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { API_ENDPOINTS, fetchAPI } from '../config/api';

const { width } = Dimensions.get('window');
const cardWidth = (width - 60) / 2;

export default function VideosScreen() {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [videoSeleccionado, setVideoSeleccionado] = useState(null);

  useEffect(() => {
    cargarVideos();
  }, []);

  const cargarVideos = async () => {
    setLoading(true);
    const response = await fetchAPI(API_ENDPOINTS.listarVideos);
    
    if (response.success) {
      setVideos(response.videos || []);
    }
    setLoading(false);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await cargarVideos();
    setRefreshing(false);
  };

  const abrirVideo = (video) => {
    setVideoSeleccionado(video);
    setModalVisible(true);
  };

  const cerrarModal = () => {
    setModalVisible(false);
    setVideoSeleccionado(null);
  };

  const eliminarVideo = async (archivo) => {
    const showAlert = (title, message) => {
      if (Platform.OS === 'web') {
        window.alert(`${title}\n\n${message}`);
      } else {
        Alert.alert(title, message);
      }
    };

    const confirmar = async () => {
      const response = await fetchAPI(API_ENDPOINTS.eliminarVideo(archivo), {
        method: 'DELETE',
      });
      
      if (response.success) {
        setVideos(videos.filter(vid => vid.archivo !== archivo));
        cerrarModal();
        showAlert('Éxito', 'Video eliminado');
      } else {
        showAlert('Error', response.error);
      }
    };

    if (Platform.OS === 'web') {
      if (window.confirm('¿Estás seguro de eliminar este video?\n\nEsta acción no se puede deshacer.')) {
        await confirmar();
      }
    } else {
      Alert.alert(
        'Eliminar Video',
        '¿Estás seguro de eliminar este video?',
        [
          { text: 'Cancelar', style: 'cancel' },
          { text: 'Eliminar', style: 'destructive', onPress: confirmar },
        ]
      );
    }
  };

  const formatearTamano = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const renderVideo = ({ item }) => (
    <TouchableOpacity
      style={styles.videoCard}
      onPress={() => abrirVideo(item)}
    >
      <View style={styles.videoPreview}>
        <Ionicons name="videocam" size={60} color="#00d4ff" />
        <View style={styles.duracionBadge}>
          <Text style={styles.duracionText}>{item.duracion}s</Text>
        </View>
      </View>
      
      <View style={styles.videoInfo}>
        <View style={styles.videoHeader}>
          <Ionicons name="alert-circle" size={14} color="#ff4757" />
          <Text style={styles.videoLinea} numberOfLines={1}>
            {item.linea.replace(/_/g, ' ')}
          </Text>
        </View>
        
        <View style={styles.videoDetail}>
          <Ionicons name="calendar" size={12} color="#5a6a8a" />
          <Text style={styles.videoDetailText}>{item.fecha}</Text>
        </View>
        
        <View style={styles.videoDetail}>
          <Ionicons name="time" size={12} color="#5a6a8a" />
          <Text style={styles.videoDetailText}>{item.hora}</Text>
        </View>
        
        <View style={styles.videoDetail}>
          <Ionicons name="document" size={12} color="#5a6a8a" />
          <Text style={styles.videoDetailText}>{formatearTamano(item.tamano)}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#00d4ff" />
        }
      >
        {/* Header */}
        <View style={styles.headerCard}>
          <View style={styles.headerIconContainer}>
            <Ionicons name="videocam" size={40} color="#ff6b35" />
          </View>
          <View style={styles.headerInfo}>
            <Text style={styles.headerTitle}>Videos de Intrusión</Text>
            <Text style={styles.headerSubtitle}>
              Grabaciones automáticas de 5 segundos
            </Text>
          </View>
        </View>

        {/* Contador */}
        <View style={styles.contadorCard}>
          <Ionicons name="film" size={24} color="#00d4ff" />
          <Text style={styles.contadorText}>
            {videos.length} {videos.length === 1 ? 'video' : 'videos'}
          </Text>
        </View>

        {/* Lista de videos */}
        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#00d4ff" />
            <Text style={styles.loadingText}>Cargando videos...</Text>
          </View>
        ) : videos.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Ionicons name="videocam-off" size={80} color="#3a4a6a" />
            <Text style={styles.emptyText}>No hay videos de intrusión</Text>
            <Text style={styles.emptySubtext}>
              Los videos se guardan automáticamente cuando se detecta un intruso
            </Text>
          </View>
        ) : (
          <FlatList
            data={videos}
            renderItem={renderVideo}
            keyExtractor={(item) => item.id.toString()}
            numColumns={2}
            scrollEnabled={false}
            columnWrapperStyle={styles.row}
          />
        )}
      </ScrollView>

      {/* Modal de video */}
      <Modal
        visible={modalVisible}
        transparent
        animationType="fade"
        onRequestClose={cerrarModal}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            {videoSeleccionado && (
              <>
                <View style={styles.modalHeader}>
                  <Text style={styles.modalTitle}>Video de Intrusión</Text>
                  <TouchableOpacity onPress={cerrarModal}>
                    <Ionicons name="close" size={24} color="#ffffff" />
                  </TouchableOpacity>
                </View>

                {/* Video player */}
                <View style={styles.videoContainer}>
                  <TouchableOpacity
                    style={styles.videoPlayerButton}
                    onPress={() => {
                      if (Platform.OS === 'web') {
                        window.open(API_ENDPOINTS.obtenerVideo(videoSeleccionado.archivo), '_blank');
                      }
                    }}
                  >
                    <Ionicons name="play-circle" size={80} color="#00d4ff" />
                    <Text style={styles.playVideoText}>
                      Reproducir Video
                    </Text>
                    <Text style={styles.playVideoSubtext}>
                      Se abrirá en nueva pestaña
                    </Text>
                  </TouchableOpacity>
                </View>

                {/* Información */}
                <View style={styles.modalInfo}>
                  <View style={styles.modalInfoRow}>
                    <Ionicons name="alert-circle" size={18} color="#ff4757" />
                    <Text style={styles.modalInfoLabel}>Línea:</Text>
                    <Text style={styles.modalInfoValue}>
                      {videoSeleccionado.linea.replace(/_/g, ' ')}
                    </Text>
                  </View>

                  <View style={styles.modalInfoRow}>
                    <Ionicons name="calendar" size={18} color="#00d4ff" />
                    <Text style={styles.modalInfoLabel}>Fecha:</Text>
                    <Text style={styles.modalInfoValue}>{videoSeleccionado.fecha}</Text>
                  </View>

                  <View style={styles.modalInfoRow}>
                    <Ionicons name="time" size={18} color="#00d4ff" />
                    <Text style={styles.modalInfoLabel}>Hora:</Text>
                    <Text style={styles.modalInfoValue}>{videoSeleccionado.hora}</Text>
                  </View>

                  <View style={styles.modalInfoRow}>
                    <Ionicons name="film" size={18} color="#00d4ff" />
                    <Text style={styles.modalInfoLabel}>Duración:</Text>
                    <Text style={styles.modalInfoValue}>{videoSeleccionado.duracion}s</Text>
                  </View>

                  <View style={styles.modalInfoRow}>
                    <Ionicons name="document" size={18} color="#00d4ff" />
                    <Text style={styles.modalInfoLabel}>Tamaño:</Text>
                    <Text style={styles.modalInfoValue}>
                      {formatearTamano(videoSeleccionado.tamano)}
                    </Text>
                  </View>
                </View>

                {/* Botón eliminar */}
                <TouchableOpacity
                  style={styles.deleteButton}
                  onPress={() => eliminarVideo(videoSeleccionado.archivo)}
                >
                  <Ionicons name="trash" size={20} color="#ffffff" />
                  <Text style={styles.deleteButtonText}>Eliminar Video</Text>
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
    borderColor: 'rgba(255, 107, 53, 0.3)',
  },
  headerIconContainer: {
    width: 70,
    height: 70,
    backgroundColor: 'rgba(255, 107, 53, 0.15)',
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
  contadorCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(0, 212, 255, 0.1)',
    borderRadius: 15,
    padding: 15,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.3)',
  },
  contadorText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#00d4ff',
    marginLeft: 10,
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
  row: {
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  videoCard: {
    width: cardWidth,
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 15,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(255, 107, 53, 0.2)',
  },
  videoPreview: {
    width: '100%',
    height: 120,
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  duracionBadge: {
    position: 'absolute',
    bottom: 8,
    right: 8,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  duracionText: {
    color: '#ffffff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  videoInfo: {
    padding: 12,
  },
  videoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  videoLinea: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#ff4757',
    marginLeft: 6,
    flex: 1,
  },
  videoDetail: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  videoDetailText: {
    fontSize: 11,
    color: '#8a9ab0',
    marginLeft: 6,
  },

  // Modal
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    justifyContent: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: '#14233c',
    borderRadius: 20,
    padding: 20,
    maxWidth: 600,
    alignSelf: 'center',
    width: '100%',
    maxHeight: '90%',
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
  videoContainer: {
    width: '100%',
    height: 300,
    backgroundColor: '#000',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  videoPlayerButton: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  playVideoText: {
    color: '#00d4ff',
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 15,
  },
  playVideoSubtext: {
    color: '#5a6a8a',
    fontSize: 12,
    marginTop: 5,
  },
  modalInfo: {
    marginBottom: 20,
  },
  modalInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(90, 106, 138, 0.2)',
  },
  modalInfoLabel: {
    fontSize: 14,
    color: '#5a6a8a',
    marginLeft: 10,
    width: 80,
  },
  modalInfoValue: {
    fontSize: 14,
    color: '#ffffff',
    fontWeight: '600',
    flex: 1,
  },
  deleteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ff4757',
    borderRadius: 12,
    padding: 15,
    gap: 10,
  },
  deleteButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

