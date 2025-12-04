import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Image,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

export default function LoginScreen({ navigation }) {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [mostrarContrasena, setMostrarContrasena] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleLogin = () => {
    if (!usuario.trim() || !contrasena.trim()) {
      Alert.alert('Error', 'Por favor ingrese usuario y contraseña');
      return;
    }

    setLoading(true);
    
    // Simulación de autenticación
    setTimeout(() => {
      setLoading(false);
      if (usuario === 'admin' && contrasena === 'admin') {
        navigation.replace('Home');
      } else {
        Alert.alert('Error', 'Credenciales incorrectas\n\nUse: admin / admin');
      }
    }, 1000);
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      {/* Fondo con gradiente simulado */}
      <View style={styles.backgroundGradient}>
        <View style={styles.gradientOverlay} />
      </View>

      {/* Partículas decorativas */}
      <View style={styles.particles}>
        {[...Array(20)].map((_, i) => (
          <View
            key={i}
            style={[
              styles.particle,
              {
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: Math.random() * 4 + 2,
                height: Math.random() * 4 + 2,
                opacity: Math.random() * 0.5 + 0.1,
              },
            ]}
          />
        ))}
      </View>

      <View style={styles.content}>
        {/* Logo */}
        <View style={styles.logoContainer}>
          <Image
            source={require('../../assets/logo.png')}
            style={styles.logo}
            resizeMode="contain"
          />
        </View>

        {/* Formulario */}
        <View style={styles.formContainer}>
          <Text style={styles.welcomeText}>Bienvenido</Text>
          <Text style={styles.subtitleText}>Sistema de Vigilancia Inteligente</Text>

          {/* Campo Usuario */}
          <View style={styles.inputContainer}>
            <Ionicons name="person-outline" size={22} color="#00d4ff" style={styles.inputIcon} />
            <TextInput
              style={styles.input}
              placeholder="Usuario"
              placeholderTextColor="#5a6a8a"
              value={usuario}
              onChangeText={setUsuario}
              autoCapitalize="none"
              autoCorrect={false}
            />
          </View>

          {/* Campo Contraseña */}
          <View style={styles.inputContainer}>
            <Ionicons name="lock-closed-outline" size={22} color="#00d4ff" style={styles.inputIcon} />
            <TextInput
              style={styles.input}
              placeholder="Contraseña"
              placeholderTextColor="#5a6a8a"
              value={contrasena}
              onChangeText={setContrasena}
              secureTextEntry={!mostrarContrasena}
              autoCapitalize="none"
            />
            <TouchableOpacity
              onPress={() => setMostrarContrasena(!mostrarContrasena)}
              style={styles.eyeIcon}
            >
              <Ionicons
                name={mostrarContrasena ? 'eye-outline' : 'eye-off-outline'}
                size={22}
                color="#5a6a8a"
              />
            </TouchableOpacity>
          </View>

          {/* Botón de ingreso */}
          <TouchableOpacity
            style={[styles.loginButton, loading && styles.loginButtonDisabled]}
            onPress={handleLogin}
            disabled={loading}
          >
            {loading ? (
              <Text style={styles.loginButtonText}>Ingresando...</Text>
            ) : (
              <>
                <Text style={styles.loginButtonText}>INGRESAR</Text>
                <Ionicons name="arrow-forward" size={20} color="#0a1628" />
              </>
            )}
          </TouchableOpacity>

          {/* Olvidó contraseña */}
          <TouchableOpacity style={styles.forgotPassword}>
            <Text style={styles.forgotPasswordText}>¿Olvidó su contraseña?</Text>
          </TouchableOpacity>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>© 2025 Apptelink Vision</Text>
          <Text style={styles.versionText}>v1.0.0</Text>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a1628',
  },
  backgroundGradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: '#0a1628',
  },
  gradientOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: height * 0.5,
    backgroundColor: 'rgba(0, 212, 255, 0.05)',
    borderBottomLeftRadius: 100,
    borderBottomRightRadius: 100,
  },
  particles: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  particle: {
    position: 'absolute',
    backgroundColor: '#00d4ff',
    borderRadius: 50,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 30,
  },
  logoContainer: {
    marginBottom: 40,
    alignItems: 'center',
    shadowColor: '#00d4ff',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
  },
  logo: {
    width: width * 0.7,
    height: 150,
    maxWidth: 350,
  },
  formContainer: {
    width: '100%',
    maxWidth: 400,
    backgroundColor: 'rgba(20, 35, 60, 0.8)',
    borderRadius: 24,
    padding: 30,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.2)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitleText: {
    fontSize: 14,
    color: '#5a6a8a',
    textAlign: 'center',
    marginBottom: 30,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(10, 22, 40, 0.8)',
    borderRadius: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.15)',
    paddingHorizontal: 16,
  },
  inputIcon: {
    marginRight: 12,
  },
  input: {
    flex: 1,
    height: 55,
    color: '#ffffff',
    fontSize: 16,
  },
  eyeIcon: {
    padding: 8,
  },
  loginButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#00d4ff',
    borderRadius: 12,
    height: 55,
    marginTop: 10,
    gap: 8,
    shadowColor: '#00d4ff',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  loginButtonDisabled: {
    backgroundColor: '#2a5a6a',
  },
  loginButtonText: {
    color: '#0a1628',
    fontSize: 16,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  forgotPassword: {
    marginTop: 20,
    alignItems: 'center',
  },
  forgotPasswordText: {
    color: '#00d4ff',
    fontSize: 14,
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    alignItems: 'center',
  },
  footerText: {
    color: '#3a4a6a',
    fontSize: 12,
  },
  versionText: {
    color: '#2a3a5a',
    fontSize: 10,
    marginTop: 4,
  },
});

