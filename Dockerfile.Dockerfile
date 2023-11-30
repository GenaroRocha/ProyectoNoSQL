# Usa la imagen oficial de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala virtualenv para crear entornos virtuales
RUN pip install virtualenv

# Crea un entorno virtual llamado 'nba'
RUN virtualenv nba

# Activa el entorno virtual
ENV VIRTUAL_ENV=/app/nba
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copia el contenido local al contenedor en /app
COPY . /app

# Instala las dependencias dentro del entorno virtual
RUN pip install -r requirements.txt
