# Usa la imagen oficial de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido local al contenedor en /app
COPY . /app

# Instala las dependencias dentro del entorno virtual
RUN pip install -r requirements.txt

# Comando predeterminado para ejecutar tus scripts cuando se inicie el contenedor
CMD ["sh", "-c", "python SuperMongo2.py && python updataneo.py"]
