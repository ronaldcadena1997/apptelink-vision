import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import LoginScreen from './src/screens/LoginScreen';
import HomeScreen from './src/screens/HomeScreen';
import CamaraScreen from './src/screens/CamaraScreen';
import ConfiguracionScreen from './src/screens/ConfiguracionScreen';
import IntrusosScreen from './src/screens/IntrusosScreen';
import VideosScreen from './src/screens/VideosScreen';
import MonitoreoScreen from './src/screens/MonitoreoScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator
        initialRouteName="Login"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#0a1628',
          },
          headerTintColor: '#00d4ff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
          contentStyle: {
            backgroundColor: '#0a1628',
          },
        }}
      >
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ 
            title: 'ApptelinkVision',
            headerLeft: () => null,
            gestureEnabled: false,
          }}
        />
        <Stack.Screen
          name="Camara"
          component={CamaraScreen}
          options={{ title: 'Cámara de Vigilancia' }}
        />
        <Stack.Screen
          name="Configuracion"
          component={ConfiguracionScreen}
          options={{ title: 'Configuración de Sectores' }}
        />
        <Stack.Screen
          name="Intrusos"
          component={IntrusosScreen}
          options={{ title: 'Imágenes de Intrusos' }}
        />
        <Stack.Screen
          name="Videos"
          component={VideosScreen}
          options={{ title: 'Videos de Intrusión' }}
        />
        <Stack.Screen
          name="Monitoreo"
          component={MonitoreoScreen}
          options={{ title: 'Monitoreo General' }}
          initialParams={{ conCercas: false }}
        />
        <Stack.Screen
          name="MonitoreoCercas"
          component={MonitoreoScreen}
          options={{ title: 'Monitoreo con Cercas' }}
          initialParams={{ conCercas: true }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

