const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Configurar projectRoot y watchFolders
config.projectRoot = __dirname;
config.watchFolders = [
  __dirname,
  // Incluir node_modules de expo para que Metro pueda acceder a @expo/cli
  path.join(__dirname, 'node_modules'),
  path.join(__dirname, 'node_modules', 'expo', 'node_modules'),
];

// Configurar resolver para incluir todos los node_modules necesarios
config.resolver = {
  ...config.resolver,
  // Permitir acceso a módulos anidados de expo
  extraNodeModules: {
    ...config.resolver.extraNodeModules,
  },
};

module.exports = config;

