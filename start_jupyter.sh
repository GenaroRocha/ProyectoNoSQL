#!/bin/bash

# Iniciar Docker Compose
docker-compose up -d

# Esperar unos segundos para que el contenedor de Jupyter se inicie completamente
echo "Esperando que Jupyter Notebook se inicie..."
sleep 10

# Obtener el ID del contenedor de Jupyter
JUPYTER_CONTAINER_ID=$(docker ps -qf "ancestor=jupyter/base-notebook")

# Obtener la URL con el token de Jupyter
JUPYTER_URL=$(docker logs $JUPYTER_CONTAINER_ID 2>&1 | grep -oP 'http://127.0.0.1:8888/\?token=\K\S+')

# Abrir Jupyter Notebook en el navegador predeterminado
if command -v xdg-open > /dev/null
then
    xdg-open "http://127.0.0.1:8888/?token=$JUPYTER_URL"
elif command -v open > /dev/null
then
    open "http://127.0.0.1:8888/?token=$JUPYTER_URL"
else
    echo "No se puede abrir el navegador automáticamente. Por favor, abre manualmente http://127.0.0.1:8888/?token=$JUPYTER_URL"
fi
