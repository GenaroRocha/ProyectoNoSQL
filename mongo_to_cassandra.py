from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

# Conexión a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['nba']
mongo_collection = mongo_db['player_data']

# Conexión a Cassandra en el puerto 9042
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()

# Crear keyspace y tabla si no existen
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS nba WITH replication = {
        'class': 'SimpleStrategy', 
        'replication_factor': '1'
    }
""")
session.execute("""
    CREATE TABLE IF NOT EXISTS nba.player_stats (
        id int PRIMARY KEY,
        player_name text,
        age int,
        games int,
        games_started int,
        minutes_played int,
        field_goals int,
        field_attempts int,
        field_percent text,
        three_fg int,
        three_attempts int,
        three_percent text,
        two_fg int,
        two_attempts int,
        two_percent text,
        effect_fg_percent text,
        ft int,
        fta int,
        ft_percent text,
        ORB int,
        DRB int,
        TRB int,
        AST int,
        STL int,
        BLK int,
        TOV int,
        PF int,
        PTS int,
        team text,
        season int
    )
""")

# Función para insertar datos en Cassandra
def insert_into_cassandra(data):
    prepared = session.prepare("""
        INSERT INTO nba.player_stats (id, player_name, age, games, games_started, minutes_played, field_goals, field_attempts, field_percent, three_fg, three_attempts, three_percent, two_fg, two_attempts, two_percent, effect_fg_percent, ft, fta, ft_percent, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, team, season)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """)
    session.execute(prepared, (data['id'], data['player_name'], data['age'], data['games'], data['games_started'], data['minutes_played'], data['field_goals'], data['field_attempts'], data['field_percent'], data['three_fg'], data['three_attempts'], data['three_percent'], data['two_fg'], data['two_attempts'], data['two_percent'], data['effect_fg_percent'], data['ft'], data['fta'], data['ft_percent'], data['ORB'], data['DRB'], data['TRB'], data['AST'], data['STL'], data['BLK'], data['TOV'], data['PF'], data['PTS'], data['team'], data['season']))

# Transferir datos de MongoDB a Cassandra
for data in mongo_collection.find():
    insert_into_cassandra(data)
