import requests
from pymongo import MongoClient

# Realizar la solicitud a la API
for season in range(2010, 2024):
	response = requests.get('https://nba-stats-db.herokuapp.com/api/playerdata/season/' + str(season))
	data = response.json()

	# Conectar a MongoDB
	client = MongoClient('mongodb://localhost:27017/')
	db = client['nba']
	collection = db['player_data']

	# Insertar datos en MongoDB
	collection.insert_many(data['results'])
 
