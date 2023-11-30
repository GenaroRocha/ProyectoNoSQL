from pymongo import MongoClient
from neo4j import GraphDatabase
#from py2neo import Graph

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['nba']
collection = db['player_data']

# Fetch data from MongoDB collection
mongo_data = collection.find()

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "neo"
driver = GraphDatabase.driver(uri, auth=(username, password))

##################################
########## Create nodes ##########
##################################
players = []
teams = []

def create_player_node(tx, props):
    tx.run("CREATE (n:Player)"
    	   "SET n += $props", props=props)

def create_team_node(tx, props):
    tx.run("CREATE (n:Team)"
    	   "SET n += $props", props=props)

#with driver.session() as session:
	#player_0 = list(mongo_data)[1]
	#player_0.pop('_id') # Removes object id
	#player_0.pop('id')
	#session.execute_write(create_player_node, player_0)

# Add a node for each json in the db
with driver.session() as session:
	for doc in mongo_data:
		# Player nodes
		if doc['type'] == 'Player':
			# Removes id and object id
			doc.pop('_id')
			doc.pop('id')
			players.append(doc)
			session.execute_write(create_player_node, doc)
		# Team nodes
		elif doc['type'] == 'Team':
			# Removes id and object id
			doc.pop('_id')
			doc.pop('id')
			# Removes player list
			#doc.pop('players')
			teams.append(doc)
			session.execute_write(create_team_node, doc)


##################################
########## Create edges ##########
##################################
def create_edges(tx):
	tx.run("""
		   MATCH (p:Player),(t:Team)
		   WHERE p.team = t.team_name
	  	   CREATE (p)-[:PART_OF]->(t);
	  	   """)

# Add an edge going from each player to his team
with driver.session() as session:
	session.execute_write(create_edges)
