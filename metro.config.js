const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Configurar projectRoot y watchFolders para evitar problemas con módulos globales
config.projectRoot = __dirname;
config.watchFolders = [__dirname];

// Asegurar que Metro solo busque en el proyecto
config.resolver = {
  ...config.resolver,
  blockList: [
    // Bloquear acceso a módulos globales fuera del proyecto
    /.*\/node_modules\/.*\/node_modules\/.*/,
  ],
};

module.exports = config;

