# Usa la imagen base de Jupyter Notebook
FROM jupyter/base-notebook

# Establece el directorio de trabajo
WORKDIR /home/jovyan

# Copia el archivo de requisitos en el contenedor
COPY requirements.txt ./

# Instala las bibliotecas desde el archivo de requisitos
RUN pip install --requirement requirements.txt

# Elimina el archivo de requisitos copiado
RUN rm requirements.txt

# Copia el contenido local al contenedor
COPY . /home/jovyan
