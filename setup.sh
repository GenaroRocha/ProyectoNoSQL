#!/bin/bash

# Crear las carpetas necesarias
mkdir -p ./data/neo4j/data
mkdir -p ./data/neo4j/logs
mkdir -p ./data/neo4j/import
mkdir -p ./data/neo4j/plugins

# Mover el archivo APOC .jar a la carpeta de plugins
mv ./apoc-4.4.0.23-all.jar ./data/neo4j/plugins/