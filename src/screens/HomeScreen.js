import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  ScrollView,
  Image,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const { width } = Dimensions.get('window');
const cardWidth = width > 600 ? (width - 90) / 2 : width - 60;

const menuOptions = [
  {
    id: 1,
    title: 'Cámara de Vigilancia',
    subtitle: 'Monitoreo en tiempo real',
    icon: 'videocam',
    screen: 'Camara',
    gradient: ['#00d4ff', '#0099cc'],
    iconColor: '#00d4ff',
  },
  {
    id: 2,
    title: 'Configuración de Sectores',
    subtitle: 'Zonas de detección',
    icon: 'settings',
    screen: 'Configuracion',
    gradient: ['#ff6b35', '#cc5528'],
    iconColor: '#ff6b35',
  },
  {
    id: 3,
    title: 'Imágenes de Intrusos',
    subtitle: 'Alertas capturadas',
    icon: 'warning',
    screen: 'Intrusos',
    gradient: ['#ff4757', '#cc3945'],
    iconColor: '#ff4757',
  },
  {
    id: 4,
    title: 'Videos de Intrusión',
    subtitle: 'Grabaciones de 5 segundos',
    icon: 'film',
    screen: 'Videos',
    gradient: ['#ff6b35', '#cc5528'],
    iconColor: '#ff6b35',
  },
  {
    id: 5,
    title: 'Monitoreo General',
    subtitle: 'Todas las cámaras en vivo',
    icon: 'apps',
    screen: 'Monitoreo',
    gradient: ['#00d4ff', '#0099cc'],
    iconColor: '#00d4ff',
  },
  {
    id: 6,
    title: 'Monitoreo con Cercas',
    subtitle: 'Vigilancia activa múltiple',
    icon: 'grid',
    screen: 'MonitoreoCercas',
    gradient: ['#2ed573', '#26a65a'],
    iconColor: '#2ed573',
  },
  {
    id: 7,
    title: 'Cerrar Sesión',
    subtitle: 'Salir del sistema',
    icon: 'log-out',
    screen: 'Login',
    gradient: ['#5a6a8a', '#4a5a7a'],
    iconColor: '#5a6a8a',
    isLogout: true,
  },
];

export default function HomeScreen({ navigation }) {
  const handleNavigation = (option) => {
    if (option.isLogout) {
      navigation.replace('Login');
    } else {
      navigation.navigate(option.screen);
    }
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Image
          source={require('../../assets/logo.png')}
          style={styles.headerLogo}
          resizeMode="contain"
        />
        <View style={styles.statusIndicator}>
          <View style={styles.statusDot} />
          <Text style={styles.statusText}>Sistema Activo</Text>
        </View>
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Título de sección */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Panel de Control</Text>
          <Text style={styles.sectionSubtitle}>
            Seleccione una opción para continuar
          </Text>
        </View>

        {/* Grid de opciones */}
        <View style={styles.grid}>
          {menuOptions.map((option) => (
            <TouchableOpacity
              key={option.id}
              style={[
                styles.card,
                { width: cardWidth },
                option.isLogout && styles.logoutCard,
              ]}
              onPress={() => handleNavigation(option)}
              activeOpacity={0.8}
            >
              <View
                style={[
                  styles.iconContainer,
                  { backgroundColor: `${option.iconColor}15` },
                ]}
              >
                <Ionicons
                  name={option.icon}
                  size={40}
                  color={option.iconColor}
                />
              </View>
              <View style={styles.cardContent}>
                <Text style={styles.cardTitle}>{option.title}</Text>
                <Text style={styles.cardSubtitle}>{option.subtitle}</Text>
              </View>
              <View style={styles.arrowContainer}>
                <Ionicons
                  name="chevron-forward"
                  size={24}
                  color={option.iconColor}
                />
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Estadísticas rápidas */}
        <View style={styles.statsContainer}>
          <Text style={styles.statsTitle}>Resumen del Sistema</Text>
          <View style={styles.statsGrid}>
            <View style={styles.statItem}>
              <Ionicons name="videocam" size={24} color="#00d4ff" />
              <Text style={styles.statNumber}>4</Text>
              <Text style={styles.statLabel}>Cámaras</Text>
            </View>
            <View style={styles.statItem}>
              <Ionicons name="alert-circle" size={24} color="#ff4757" />
              <Text style={styles.statNumber}>2</Text>
              <Text style={styles.statLabel}>Alertas</Text>
            </View>
            <View style={styles.statItem}>
              <Ionicons name="shield-checkmark" size={24} color="#2ed573" />
              <Text style={styles.statNumber}>12</Text>
              <Text style={styles.statLabel}>Sectores</Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a1628',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 212, 255, 0.1)',
  },
  headerLogo: {
    width: 150,
    height: 40,
  },
  statusIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(46, 213, 115, 0.15)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#2ed573',
    marginRight: 8,
  },
  statusText: {
    color: '#2ed573',
    fontSize: 12,
    fontWeight: '600',
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  sectionHeader: {
    marginBottom: 25,
  },
  sectionTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
  },
  sectionSubtitle: {
    fontSize: 14,
    color: '#5a6a8a',
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 15,
  },
  card: {
    backgroundColor: 'rgba(20, 35, 60, 0.8)',
    borderRadius: 20,
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.15)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
    marginBottom: 5,
  },
  logoutCard: {
    borderColor: 'rgba(90, 106, 138, 0.3)',
    backgroundColor: 'rgba(30, 40, 60, 0.6)',
  },
  iconContainer: {
    width: 70,
    height: 70,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  cardContent: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  cardSubtitle: {
    fontSize: 12,
    color: '#5a6a8a',
  },
  arrowContainer: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  statsContainer: {
    marginTop: 30,
    backgroundColor: 'rgba(20, 35, 60, 0.6)',
    borderRadius: 20,
    padding: 20,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.1)',
  },
  statsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 20,
    textAlign: 'center',
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#5a6a8a',
    marginTop: 4,
  },
});

