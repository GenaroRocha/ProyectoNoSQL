import requests
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['nba']
collection = db['player_data']

for season in range(2010, 2024):
    try:
        # Realizar la solicitud a la API
        response = requests.get(f'https://nba-stats-db.herokuapp.com/api/playerdata/season/{season}')
        response.raise_for_status()  # Esto lanzará una excepción si la solicitud no fue exitosa
        data = response.json()

        # Insertar datos en MongoDB si 'results' está presente en la respuesta
        if 'results' in data:
            collection.insert_many(data['results'])
        else:
            print(f"No se encontraron resultados para la temporada {season}")
    
    except requests.RequestException as e:
        print(f"Error de solicitud para la temporada {season}: {e}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error al insertar documentos para la temporada {season}: {e}")

# Contar y mostrar el número de documentos en la colección
count = collection.count_documents({})
print(f"Total de documentos en la colección: {count}")



