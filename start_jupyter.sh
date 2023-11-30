#!/bin/bash

# Iniciar Docker Compose
docker-compose up -d

# Esperar unos segundos para que el contenedor de Jupyter se inicie completamente
echo "Esperando que Jupyter Notebook se inicie..."
sleep 20

# Obtener el ID del contenedor de Jupyter usando su nombre de contenedor
JUPYTER_CONTAINER_ID=$(docker ps -qf "name=proyectonosql-jupyter-1")

# Verificar si se encontró el ID del contenedor
if [ -z "$JUPYTER_CONTAINER_ID" ]; then
    echo "No se encontró el contenedor de Jupyter. Verifica si está en ejecución."
    exit 1
fi

# Obtener la URL con el token de Jupyter
JUPYTER_URL=$(docker logs $JUPYTER_CONTAINER_ID 2>&1 | grep "token=" | head -n 1 | awk -F"token=" '{print $2}' | awk '{print $1}')

# Verificar si se extrajo el token
if [ -z "$JUPYTER_URL" ]; then
    echo "No se pudo obtener el token. Por favor, verifica los logs del contenedor para obtener el token."
    exit 1
fi

# Abrir Jupyter Notebook en el navegador predeterminado
if command -v xdg-open > /dev/null; then
    xdg-open "http://127.0.0.1:8888/notebooks/proyecto.ipynb?token=$JUPYTER_URL"
elif command -v open > /dev/null; then
    open "http://127.0.0.1:8888/notebooks/proyecto.ipynb?token=$JUPYTER_URL"
else
    echo "No se puede abrir el navegador automáticamente. Por favor, abre manualmente http://127.0.0.1:8888/notebooks/proyecto.ipynb?token=$JUPYTER_URL"
fi
