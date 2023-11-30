

---

# ProyectoNoSQL - NBA

!(https://www.wallpaperflare.com/static/862/992/3/kentucky-basketball-2015-ncaa-final-four-wallpaper.jpg)

## Descripción
Este proyecto utiliza tecnologías NoSQL para manejar y analizar datos de la NBA. El flujo de datos se maneja a través de un datalake en MongoDB, se transforma y almacena en Cassandra, y se crea un grafo en Neo4J para análisis avanzados.

## Configuración y Ejecución

### Clonar el Repositorio
Para comenzar, clone este repositorio en su máquina local:

```bash
git clone https://github.com/GenaroRocha/ProyectoNoSQL
cd ProyectoNoSQL
```

### Configuración del Entorno
Antes de ejecutar el proyecto, asegúrese de tener Docker y Docker Compose instalados. Luego, siga los siguientes pasos para configurar el entorno:

1. **Ejecutar el Script de Configuración** (si es aplicable):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Iniciar Jupyter Notebook**:
   - Asigne permisos de ejecución al script de inicio de Jupyter:
     ```bash
     chmod +x start_jupyter.sh
     ```
   - Ejecute el script para iniciar Jupyter y abrirlo automáticamente en su navegador:
     ```bash
     ./start_jupyter.sh
     ```

### Trabajar con Jupyter Notebook
Una vez que Jupyter Notebook esté en ejecución, se abrirá en su navegador web. Desde allí, podrá acceder y ejecutar el archivo `proyecto.ipynb`, que contiene el código y los análisis para el proyecto.

### Interacción con las Bases de Datos
El proyecto utiliza MongoDB, Cassandra y Neo4J. Asegúrese de que los servicios correspondientes estén en ejecución y accesibles a través de Jupyter Notebook para realizar operaciones de base de datos.

## Primera Parte: Vaciado en Mongo
Describa aquí los pasos específicos o scripts para trabajar con MongoDB, incluyendo cómo vaciar datos en el datalake.

## Segunda Parte: Transformación con Cassandra
Instrucciones sobre cómo transformar y mover los datos a Cassandra.

## Tercera Parte: Creación del Grafo en Neo4J
Pasos para crear y analizar el grafo en Neo4J a partir de los datos existentes.

---

