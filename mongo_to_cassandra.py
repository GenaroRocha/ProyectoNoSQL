from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

# MongoDB connection setup
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['nba']
mongo_collection = mongo_db['player_data']

# Cassandra connection setup
cluster = Cluster(['localhost'])
cassandra_session = cluster.connect()

# Create keyspace and table in Cassandra if they don't exist
cassandra_session.execute("""
    CREATE KEYSPACE IF NOT EXISTS nba WITH replication = { 
        'class': 'SimpleStrategy', 
        'replication_factor': '1' 
    }
""")
cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS nba.player_data (
        id int PRIMARY KEY,
        type text,
        team_name text,
        players list<text>
    )
""")

# Function to insert data into Cassandra
def insert_into_cassandra(data):
    # Assuming data is a dictionary containing the player data
    # Adjust field names and types according to your data model and requirements
    prepared = cassandra_session.prepare("""
        INSERT INTO nba.player_data (id, type, team_name, players)
        VALUES (?, ?, ?, ?)
    """)
    batch = BatchStatement()
    batch.add(prepared, (data['id'], data['type'], data['team_name'], data['players']))
    cassandra_session.execute(batch)

# Fetch data from MongoDB collection
mongo_data = mongo_collection.find()

# Transfer data to Cassandra
for data in mongo_data:
    insert_into_cassandra(data)
