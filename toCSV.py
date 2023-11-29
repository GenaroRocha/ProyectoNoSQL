import pandas as pd
from pymongo import MongoClient

# Configura la conexión a MongoDB (ajusta según sea necesario)
client = MongoClient('mongodb://localhost:27017/')
db = client['nba']
collection = db['player_data']

# Extrae los datos de la colección
data = list(collection.find())

# Convierte los datos a un DataFrame de pandas
df = pd.DataFrame(data)

# Verifica si la columna '_id' existe y elimínala si es necesario
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# Guarda el DataFrame en un archivo CSV
df.to_csv('NBA.csv', index=False)

print("Los datos han sido guardados en 'NBA.csv'")
