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


'''
@staticmethod
def _create_and_return_greeting(tx, message):
    result = tx.run("CREATE (a:Greeting) "
                    "SET a.message = $message "
                    "RETURN a.message + ', from node ' + id(a)", message=message)
    return result.single()[0]

with driver.session() as session:
    greeting = session.execute_write(_create_and_return_greeting, "Hello world")
    print(greeting)

driver.close()
'''


'''
# Set type por all players in the database
db.player_data.updateMany({}, {$set: {'type': "Player"}})

# Find all teams
db.player_data.aggregate([ { $group: {_id: "$team"} }  ])

# Find all seasons
db.player_data.aggregate([ { $group: {_id: "$team"} }  ])

# Find all teams from each team


# Insert teams
db.player_data.insertMany(
[
{ 'id': 10000, 'team_name': 'MEM', 'type': 'Team' },
{ 'id': 10001, 'team_name': 'BOS', 'type': 'Team' },
{ 'id': 10002, 'team_name': 'BRK', 'type': 'Team' },
{ 'id': 10003, 'team_name': 'TOR', 'type': 'Team' },
{ 'id': 10004, 'team_name': 'NJN', 'type': 'Team' },
{ 'id': 10005, 'team_name': 'ATL', 'type': 'Team' },
{ 'id': 10006, 'team_name': 'DAL', 'type': 'Team' },
{ 'id': 10007, 'team_name': 'PHI', 'type': 'Team' },
{ 'id': 10008, 'team_name': 'NYK', 'type': 'Team' },
{ 'id': 10009, 'team_name': 'HOU', 'type': 'Team' }
])



{
    id: 7562,
    type: 'Team',
    team_name: 'HOU',
    players: [
	  'Tarik Black', 'Daishen Nix', 'Chris Chiozza', 'Kenneth Faried', 'Carmelo Anthony', 'Kevin Martin',
	  'Marquese Chriss', 'Lou Williams', 'Eric Gordon', 'Dwight Howard', 'Jeff Green', 'Frank Kaminsky',
	  'Clint Capela', 'Pops Mensah-Bonsu', 'Darius Days', 'Alexey Shved', 'James Harden', 'Troy Daniels',
	  'Nick Johnson', 'Cameron Reynolds', 'William Howard', 'Rodions Kurucs', 'Tari Eason', 'Josh Christopher',
	  'Marcus Camby', 'Thomas Robinson', 'Chris Clemons', 'Pablo Prigioni', 'Kyle Wiltjer', 'Cameron Oliver',
	  'Kyle Lowry', 'Danuel House Jr.', 'Isaiah Hartenstein', 'Courtney Fortson', 'Marcus Thornton', 
	  'Khyri Thomas', 'Aaron Brooks', 'Goran Dragić', 'Sam Dekker', 'Luis Scola', 'Kenyon Martin Jr.',
	  'Austin Rivers', 'Kevin Porter Jr.', 'Courtney Lee', 'Yao Ming', 'Toney Douglas', 'Tyler Ennis',
	  'Thabo Sefolosha', 'Ray Spalding', 'Demetrius Jackson', 'D.J. Wilson', 'DeMarre Carroll', 'Samuel Dalembert',
	  'Michael Beasley', 'Sterling Brown', 'Jae'Sean Tate', 'Aaron Jackson', 'Russell Westbrook',
	  'Jared Jeffries', 'Cole Aldrich', 'Tyson Chandler', 'Isaiah Canaan', 'Jordan Hamilton', 'Terrence Williams',
	  'Jalen Green', 'Bruno Fernando', 'Jabari Smith Jr.', 'Troy Williams', 'John Wall', 'Ish Smith', 'Ty Lawson', 
	  'Michael Carter-Williams', 'Markel Brown', 'Zhou Qi', 'Carl Landry', 'Brandon Knight', 'Brodric Thomas',
	  'David Andersen', 'Mike Harris', 'Brian Cook', 'Jeremy Lin', 'Francisco García', 'Terrence Jones',
	  'Corey Brewer', 'Ömer Aşık', 'Josh Powell', 'Avery Bradley', 'David Nwaba', 'Will Conroy', 
	  'Jermaine Taylor', 'Ben McLemore', 'Joe Johnson', 'Brad Miller', 'Hasheem Thabeet', 'Montrezl Harrell',
	  'Carlos Delfino', 'Tim Quarterman', 'Iman Shumpert', 'Chuck Hayes', 'Chase Budinger', 'DeMarcus Cousins',
	  'Briante Weber', 'Ronnie Brewer', 'Gerald Green', 'Trevelin Queen', 'Gary Clark', 'Kostas Papanikolaou',
	  'Tim Ohlbrecht', 'Anthony Lamb', 'Michael Frazier', 'Tracy McGrady', 'Jeff Adrien', 'Marcus Morris',
	  'Shane Battier', 'Ryan Anderson', 'Christian Wood', 'Armoni Brooks', 'Earl Boykins', 'R.J. Hunter',
	  'K.J. McDaniels', 'Isaiah Taylor', 'Garrett Temple', 'Jordan Hill', 'Donatas Motiejūnas', 'P.J. Tucker',
	  'Mason Jones', 'Chinanu Onuaku', 'Omri Casspi', 'TyTy Washington Jr.', 'Jonny Flynn', 'Jason Terry',
	  'Justin Patton', 'Robert Covington', 'D.J. Augustin', 'Boban Marjanović', 'Chandler Parsons',
	  'Daniel Theis', 'Garrison Mathews', 'Daequan Cook', 'Dennis Schröder', 'Vince Edwards', 'Trevor Hudgins',
	  'Joey Dorsey', 'Greg Smith', 'Patrick Patterson', 'James Ennis III', 'Hilton Armstrong', 'Kelly Olynyk',
	  'Bruno Caboclo', 'Chris Paul', 'Victor Oladipo', 'Patrick Beverley', 'Nenê', 'Scott Machado', 'Alperen Şengün', 
	  'Luc Mbah a Moute', 'Usman Garuba', 'Trevor Ariza', 'Bobby Brown', 'DaQuan Jeffries', 'James Anderson',
	  'Josh Smith', 'James Nunnally'
    ]
    
    player_name: 'Will Conroy',
    games: 5,
    games_started: 0,
    minutes_played: 36,
    field_goals: 3,
    field_attempts: 10,
    field_percent: '0.300',
    three_fg: 0,
    three_attempts: 3,
    three_percent: '0.000',
    two_fg: 3,
    two_attempts: 7,
    two_percent: '0.429',
    effect_fg_percent: '0.300',
    ft: 0,
    fta: 2,
    ft_percent: '0.000',
    ORB: 0,
    DRB: 3,
    TRB: 3,
    AST: 7,
    STL: 0,
    BLK: 0,
    TOV: 4,
    PF: 5,
    PTS: 6,
    team: 'HOU',
    season: 2010,
    type: 'Person
}


# label: age, 
# nodes: players, seasons, teams


db.nba.aggregate([
	{ $match: {<conditions>} },
	{ $project: {team: 1} },
	{ $group: {_id: "$team"}, [var]:{<operation>} },
	{ $sort: {_id: "$<field>"}, [var]:{<operation>} },
	{ $out: "<new_collection>" }
])
'''

'''
{ _id: 'HOU', unique: 'Andrew Goudelock' },
  { _id: 'HOU', unique: 'Tarik Black' },
  { _id: 'HOU', unique: 'Daishen Nix' },
  { _id: 'HOU', unique: 'Chris Chiozza' },
  { _id: 'HOU', unique: 'Kenneth Faried' },
  { _id: 'HOU', unique: 'Carmelo Anthony' },
  { _id: 'HOU', unique: 'Kevin Martin' },
  { _id: 'HOU', unique: 'Marquese Chriss' },
  { _id: 'HOU', unique: 'Lou Williams' },
  { _id: 'HOU', unique: 'Eric Gordon' },
  { _id: 'HOU', unique: 'Dwight Howard' },
  { _id: 'HOU', unique: 'Jeff Green' },
  { _id: 'HOU', unique: 'Frank Kaminsky' },
  { _id: 'HOU', unique: 'Clint Capela' },
  { _id: 'HOU', unique: 'Pops Mensah-Bonsu' },
  { _id: 'HOU', unique: 'Darius Days' },
  { _id: 'HOU', unique: 'Alexey Shved' },
  { _id: 'HOU', unique: 'James Harden' },
  { _id: 'HOU', unique: 'Troy Daniels' },
  { _id: 'HOU', unique: 'Nick Johnson' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Cameron Reynolds' },
  { _id: 'HOU', unique: 'William Howard' },
  { _id: 'HOU', unique: 'Rodions Kurucs' },
  { _id: 'HOU', unique: 'Tari Eason' },
  { _id: 'HOU', unique: 'Josh Christopher' },
  { _id: 'HOU', unique: 'Marcus Camby' },
  { _id: 'HOU', unique: 'Thomas Robinson' },
  { _id: 'HOU', unique: 'Chris Clemons' },
  { _id: 'HOU', unique: 'Pablo Prigioni' },
  { _id: 'HOU', unique: 'Kyle Wiltjer' },
  { _id: 'HOU', unique: 'Cameron Oliver' },
  { _id: 'HOU', unique: 'Kyle Lowry' },
  { _id: 'HOU', unique: 'Danuel House Jr.' },
  { _id: 'HOU', unique: 'Isaiah Hartenstein' },
  { _id: 'HOU', unique: 'Courtney Fortson' },
  { _id: 'HOU', unique: 'Marcus Thornton' },
  { _id: 'HOU', unique: 'Khyri Thomas' },
  { _id: 'HOU', unique: 'Brandan Wright' },
  { _id: 'HOU', unique: 'Aaron Brooks' },
  { _id: 'HOU', unique: 'Goran Dragić' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Sam Dekker' },
  { _id: 'HOU', unique: 'Luis Scola' },
  { _id: 'HOU', unique: 'Kenyon Martin Jr.' },
  { _id: 'HOU', unique: 'Austin Rivers' },
  { _id: 'HOU', unique: 'Kevin Porter Jr.' },
  { _id: 'HOU', unique: 'Courtney Lee' },
  { _id: 'HOU', unique: 'Yao Ming' },
  { _id: 'HOU', unique: 'Toney Douglas' },
  { _id: 'HOU', unique: 'Tyler Ennis' },
  { _id: 'HOU', unique: 'Thabo Sefolosha' },
  { _id: 'HOU', unique: 'Ray Spalding' },
  { _id: 'HOU', unique: 'Demetrius Jackson' },
  { _id: 'HOU', unique: 'D.J. Wilson' },
  { _id: 'HOU', unique: 'DeMarre Carroll' },
  { _id: 'HOU', unique: 'Samuel Dalembert' },
  { _id: 'HOU', unique: 'Michael Beasley' },
  { _id: 'HOU', unique: 'Sterling Brown' },
  { _id: 'HOU', unique: "Jae'Sean Tate" },
  { _id: 'HOU', unique: 'Aaron Jackson' },
  { _id: 'HOU', unique: 'Russell Westbrook' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Jared Jeffries' },
  { _id: 'HOU', unique: 'Cole Aldrich' },
  { _id: 'HOU', unique: 'Tyson Chandler' },
  { _id: 'HOU', unique: 'Isaiah Canaan' },
  { _id: 'HOU', unique: 'Jordan Hamilton' },
  { _id: 'HOU', unique: 'Terrence Williams' },
  { _id: 'HOU', unique: 'Jalen Green' },
  { _id: 'HOU', unique: 'Bruno Fernando' },
  { _id: 'HOU', unique: 'Jabari Smith Jr.' },
  { _id: 'HOU', unique: 'Troy Williams' },
  { _id: 'HOU', unique: 'John Wall' },
  { _id: 'HOU', unique: 'Ish Smith' },
  { _id: 'HOU', unique: 'Ty Lawson' },
  { _id: 'HOU', unique: 'Michael Carter-Williams' },
  { _id: 'HOU', unique: 'Markel Brown' },
  { _id: 'HOU', unique: 'Zhou Qi' },
  { _id: 'HOU', unique: 'Carl Landry' },
  { _id: 'HOU', unique: 'Brandon Knight' },
  { _id: 'HOU', unique: 'Brodric Thomas' },
  { _id: 'HOU', unique: 'David Andersen' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Mike Harris' },
  { _id: 'HOU', unique: 'Brian Cook' },
  { _id: 'HOU', unique: 'Jeremy Lin' },
  { _id: 'HOU', unique: 'Francisco García' },
  { _id: 'HOU', unique: 'Terrence Jones' },
  { _id: 'HOU', unique: 'Corey Brewer' },
  { _id: 'HOU', unique: 'Ömer Aşık' },
  { _id: 'HOU', unique: 'Josh Powell' },
  { _id: 'HOU', unique: 'Avery Bradley' },
  { _id: 'HOU', unique: 'David Nwaba' },
  { _id: 'HOU', unique: 'Will Conroy' },
  { _id: 'HOU', unique: 'Jermaine Taylor' },
  { _id: 'HOU', unique: 'Ben McLemore' },
  { _id: 'HOU', unique: 'Joe Johnson' },
  { _id: 'HOU', unique: 'Brad Miller' },
  { _id: 'HOU', unique: 'Hasheem Thabeet' },
  { _id: 'HOU', unique: 'Montrezl Harrell' },
  { _id: 'HOU', unique: 'Carlos Delfino' },
  { _id: 'HOU', unique: 'Tim Quarterman' },
  { _id: 'HOU', unique: 'Iman Shumpert' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Chuck Hayes' },
  { _id: 'HOU', unique: 'Chase Budinger' },
  { _id: 'HOU', unique: 'DeMarcus Cousins' },
  { _id: 'HOU', unique: 'Briante Weber' },
  { _id: 'HOU', unique: 'Ronnie Brewer' },
  { _id: 'HOU', unique: 'Gerald Green' },
  { _id: 'HOU', unique: 'Trevelin Queen' },
  { _id: 'HOU', unique: 'Gary Clark' },
  { _id: 'HOU', unique: 'Kostas Papanikolaou' },
  { _id: 'HOU', unique: 'Tim Ohlbrecht' },
  { _id: 'HOU', unique: 'Anthony Lamb' },
  { _id: 'HOU', unique: 'Michael Frazier' },
  { _id: 'HOU', unique: 'Tracy McGrady' },
  { _id: 'HOU', unique: 'Jeff Adrien' },
  { _id: 'HOU', unique: 'Marcus Morris' },
  { _id: 'HOU', unique: 'Shane Battier' },
  { _id: 'HOU', unique: 'Ryan Anderson' },
  { _id: 'HOU', unique: 'Christian Wood' },
  { _id: 'HOU', unique: 'Armoni Brooks' },
  { _id: 'HOU', unique: 'Earl Boykins' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'R.J. Hunter' },
  { _id: 'HOU', unique: 'K.J. McDaniels' },
  { _id: 'HOU', unique: 'Isaiah Taylor' },
  { _id: 'HOU', unique: 'Garrett Temple' },
  { _id: 'HOU', unique: 'Jordan Hill' },
  { _id: 'HOU', unique: 'Donatas Motiejūnas' },
  { _id: 'HOU', unique: 'P.J. Tucker' },
  { _id: 'HOU', unique: 'Mason Jones' },
  { _id: 'HOU', unique: 'Chinanu Onuaku' },
  { _id: 'HOU', unique: 'Omri Casspi' },
  { _id: 'HOU', unique: 'TyTy Washington Jr.' },
  { _id: 'HOU', unique: 'Jonny Flynn' },
  { _id: 'HOU', unique: 'Jason Terry' },
  { _id: 'HOU', unique: 'Justin Patton' },
  { _id: 'HOU', unique: 'Robert Covington' },
  { _id: 'HOU', unique: 'D.J. Augustin' },
  { _id: 'HOU', unique: 'Boban Marjanović' },
  { _id: 'HOU', unique: 'Chandler Parsons' },
  { _id: 'HOU', unique: 'Daniel Theis' },
  { _id: 'HOU', unique: 'Garrison Mathews' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Daequan Cook' },
  { _id: 'HOU', unique: 'Dennis Schröder' },
  { _id: 'HOU', unique: 'Vince Edwards' },
  { _id: 'HOU', unique: 'Trevor Hudgins' },
  { _id: 'HOU', unique: 'Joey Dorsey' },
  { _id: 'HOU', unique: 'Greg Smith' },
  { _id: 'HOU', unique: 'Patrick Patterson' },
  { _id: 'HOU', unique: 'James Ennis III' },
  { _id: 'HOU', unique: 'Hilton Armstrong' },
  { _id: 'HOU', unique: 'Kelly Olynyk' },
  { _id: 'HOU', unique: 'Bruno Caboclo' },
  { _id: 'HOU', unique: 'Chris Paul' },
  { _id: 'HOU', unique: 'Victor Oladipo' },
  { _id: 'HOU', unique: 'Patrick Beverley' },
  { _id: 'HOU', unique: 'Nenê' },
  { _id: 'HOU', unique: 'Scott Machado' },
  { _id: 'HOU', unique: 'Alperen Şengün' },
  { _id: 'HOU', unique: 'Luc Mbah a Moute' },
  { _id: 'HOU', unique: 'Usman Garuba' },
  { _id: 'HOU', unique: 'Trevor Ariza' }
]
Type "it" for more
nba> it
[
  { _id: 'HOU', unique: 'Bobby Brown' },
  { _id: 'HOU', unique: 'DaQuan Jeffries' },
  { _id: 'HOU', unique: 'James Anderson' },
  { _id: 'HOU', unique: 'Josh Smith' },
  { _id: 'HOU', unique: 'James Nunnally' },
  { _id: 'BRK', unique: 'Chris Chiozza' },
  { _id: 'BRK', unique: 'Gerald Wallace' },
  { _id: 'BRK', unique: 'Thaddeus Young' },
  { _id: 'BRK', unique: 'Kevin Durant' },
  { _id: 'BRK', unique: 'Jeff Green' },
  { _id: 'BRK', unique: 'Timothé Luwawu-Cabarrot' },
  { _id: 'BRK', unique: 'Quincy Acy' },
  { _id: 'BRK', unique: 'James Harden' },
  { _id: 'BRK', unique: 'Andrew Nicholson' },
  { _id: 'BRK', unique: 'MarShon Brooks' },
  { _id: 'BRK', unique: 'Marquis Teague' },
  { _id: 'BRK', unique: 'Rodions Kurucs' },
  { _id: 'BRK', unique: "D'Angelo Russell" },
  { _id: 'BRK', unique: 'Ben Simmons' },
  { _id: 'BRK', unique: 'Thomas Robinson' }
]
Type "it" for more
nba> it
[
  { _id: 'BRK', unique: 'Joe Harris' },
  { _id: 'BRK', unique: 'Tyler Johnson' },
  { _id: 'BRK', unique: 'Marcus Thornton' },
  { _id: 'BRK', unique: 'Seth Curry' },
  { _id: 'BRK', unique: 'Andray Blatche' },
  { _id: 'BRK', unique: 'Damion James' },
  { _id: 'BRK', unique: 'Jarrett Jack' },
  { _id: 'BRK', unique: 'Luis Scola' },
  { _id: 'BRK', unique: 'DeAndre Jordan' },
  { _id: 'BRK', unique: 'Bruce Brown' },
  { _id: 'BRK', unique: 'Edmond Sumner' },
  { _id: 'BRK', unique: 'DeMarre Carroll' },
  { _id: 'BRK', unique: 'Kris Humphries' },
  { _id: 'BRK', unique: 'Tyshawn Taylor' },
  { _id: 'BRK', unique: 'Markieff Morris' },
  { _id: 'BRK', unique: 'Henry Ellenson' },
  { _id: 'BRK', unique: 'Bojan Bogdanović' },
  { _id: 'BRK', unique: 'Allen Crabbe' },
  { _id: 'BRK', unique: 'Jamal Crawford' },
  { _id: 'BRK', unique: 'Spencer Dinwiddie' }
]
Type "it" for more
nba> it
[
  { _id: 'BRK', unique: 'Alan Anderson' },
  { _id: 'BRK', unique: 'James Johnson' },
  { _id: 'BRK', unique: 'Donta Hall' },
  { _id: 'BRK', unique: 'Markel Brown' },
  { _id: 'BRK', unique: 'Jared Dudley' },
  { _id: 'BRK', unique: 'RaiQuan Gray' },
  { _id: 'BRK', unique: 'Jason Collins' },
  { _id: 'BRK', unique: 'Sean Kilpatrick' },
  { _id: 'BRK', unique: 'Andrea Bargnani' },
  { _id: 'BRK', unique: 'Jeremy Lin' },
  { _id: 'BRK', unique: 'David Nwaba' },
  { _id: 'BRK', unique: 'Mikal Bridges' },
  { _id: 'BRK', unique: 'Džanan Musa' },
  { _id: 'BRK', unique: 'Kessler Edwards' },
  { _id: 'BRK', unique: 'Kyrie Irving' },
  { _id: 'BRK', unique: 'Moses Brown' },
  { _id: 'BRK', unique: 'Joe Johnson' },
  { _id: 'BRK', unique: 'Shane Larkin' },
  { _id: 'BRK', unique: 'Landry Shamet' },
  { _id: 'BRK', unique: 'Ed Davis' }
]
Type "it" for more
nba> it
[
  { _id: 'BRK', unique: 'Jarrett Allen' },
  { _id: 'BRK', unique: 'Yogi Ferrell' },
  { _id: 'BRK', unique: 'David Duke Jr.' },
  { _id: 'BRK', unique: 'Anthony Bennett' },
  { _id: 'BRK', unique: 'Iman Shumpert' },
  { _id: 'BRK', unique: 'Keith Bogans' },
  { _id: 'BRK', unique: 'Cameron Johnson' },
  { _id: 'BRK', unique: 'Nerlens Noel' },
  { _id: 'BRK', unique: 'Sergey Karasev' },
  { _id: 'BRK', unique: 'Wilson Chandler' },
  { _id: 'BRK', unique: 'Yuta Watanabe' },
  { _id: 'BRK', unique: 'Shaun Livingston' },
  { _id: 'BRK', unique: 'Brook Lopez' },
  { _id: 'BRK', unique: 'Nic Claxton' },
  { _id: 'BRK', unique: 'Rondae Hollis-Jefferson' },
  { _id: 'BRK', unique: 'Theo Pinson' },
  { _id: 'BRK', unique: 'Reggie Evans' },
  { _id: 'BRK', unique: 'Justin Hamilton' },
  { _id: 'BRK', unique: 'Cam Thomas' },
  { _id: 'BRK', unique: "Day'Ron Sharpe" }
]
Type "it" for more
nba> it
[
  { _id: 'BRK', unique: 'Paul Pierce' },
  { _id: 'BRK', unique: 'K.J. McDaniels' },
  { _id: 'BRK', unique: 'Garrett Temple' },
  { _id: 'BRK', unique: 'Kevin Garnett' },
  { _id: 'BRK', unique: 'Trevor Booker' },
  { _id: 'BRK', unique: 'Lance Thomas' },
  { _id: 'BRK', unique: 'Alondes Williams' },
  { _id: 'BRK', unique: 'C.J. Watson' },
  { _id: 'BRK', unique: 'Taurean Prince' },
  { _id: 'BRK', unique: 'Tornike Shengelia' },
  { _id: 'BRK', unique: 'Jason Terry' },
  { _id: 'BRK', unique: 'Jorge Gutiérrez' },
  { _id: 'BRK', unique: 'Kris Joseph' },
  { _id: 'BRK', unique: 'Randy Foye' },
  { _id: 'BRK', unique: 'Patty Mills' },
  { _id: 'BRK', unique: 'Andrei Kirilenko' },
  { _id: 'BRK', unique: 'Isaiah Whitehead' },
  { _id: 'BRK', unique: 'T.J. Warren' },
  { _id: 'BRK', unique: 'Wayne Ellington' },
  { _id: 'BRK', unique: 'Dru Smith' }
]
Type "it" for more
nba> it
[
  { _id: 'BRK', unique: 'Cory Jefferson' },
  { _id: 'BRK', unique: 'Dorian Finney-Smith' },
  { _id: 'BRK', unique: 'Tyler Zeller' },
  { _id: 'BRK', unique: 'Deron Williams' },
  { _id: 'BRK', unique: "Royce O'Neale" },
  { _id: 'BRK', unique: 'Josh Childress' },
  { _id: 'BRK', unique: 'Mirza Teletović' },
  { _id: 'BRK', unique: 'Henry Sims' },
  { _id: 'BRK', unique: 'Nik Stauskas' },
  { _id: 'BRK', unique: 'Mason Plumlee' },
  { _id: 'BRK', unique: 'Willie Reed' },
  { _id: 'BRK', unique: 'Caris LeVert' },
  { _id: 'BRK', unique: 'Archie Goodwin' },
  { _id: 'BRK', unique: 'Donald Sloan' },
  { _id: 'BRK', unique: 'Chris McCullough' },
  { _id: 'BRK', unique: 'Greivis Vásquez' },
  { _id: 'BRK', unique: 'Jeremiah Martin' },
  { _id: 'BRK', unique: 'Jerry Stackhouse' },
  { _id: 'BRK', unique: 'Justin Anderson' },
  { _id: 'DAL', unique: 'Ray Spalding' }
]
Type "it" for more
nba> it
[
  { _id: 'TOR', unique: 'Patrick Patterson' },
  { _id: 'TOR', unique: 'Hedo Türkoğlu' },
  { _id: 'TOR', unique: 'DeMarre Carroll' },
  { _id: 'TOR', unique: 'DeMar DeRozan' },
  { _id: 'TOR', unique: 'Linas Kleiza' },
  { _id: 'TOR', unique: 'Bismack Biyombo' },
  { _id: 'TOR', unique: 'Alan Anderson' },
  { _id: 'TOR', unique: 'Chris Bosh' },
  { _id: 'TOR', unique: 'James Johnson' },
  { _id: 'TOR', unique: 'Cory Joseph' },
  { _id: 'TOR', unique: 'Delon Wright' },
  { _id: 'TOR', unique: 'Jason Thompson' },
  { _id: 'TOR', unique: 'Jarrett Jack' },
  { _id: 'TOR', unique: 'Pascal Siakam' },
  { _id: 'TOR', unique: 'Luis Scola' },
  { _id: 'TOR', unique: 'Lucas Nogueira' },
  { _id: 'TOR', unique: 'Anthony Bennett' },
  { _id: 'TOR', unique: 'José Calderón' },
  { _id: 'TOR', unique: 'Amir Johnson' },
  { _id: 'TOR', unique: 'Terrence Ross' }
]
Type "it" for more
nba> it
[
  { _id: 'TOR', unique: 'Ed Davis' },
  { _id: 'TOR', unique: 'Norman Powell' },
  { _id: 'TOR', unique: 'Scottie Barnes' },
  { _id: 'TOR', unique: 'Leandro Barbosa' },
  { _id: 'TOR', unique: 'Andrea Bargnani' },
  { _id: 'TOR', unique: 'Kyle Lowry' },
  { _id: 'TOR', unique: 'Jonas Valančiūnas' },
  { _id: 'IND', unique: 'Ben Moore' },
  { _id: 'NJN', unique: 'Mario West' },
  { _id: 'NJN', unique: 'Kris Humphries' },
  { _id: 'NJN', unique: 'Larry Owens' },
  { _id: 'NJN', unique: 'Joe Smith' },
  { _id: 'NJN', unique: 'Jordan Farmar' },
  { _id: 'NJN', unique: 'Jordan Williams' },
  { _id: 'NJN', unique: 'Gerald Wallace' },
  { _id: 'NJN', unique: 'Bobby Simmons' },
  { _id: 'NJN', unique: 'Stephen Graham' },
  { _id: 'NJN', unique: 'Eduardo Nájera' },
  { _id: 'NJN', unique: 'Devin Harris' },
  { _id: 'NJN', unique: 'Travis Outlaw' }
]
Type "it" for more
nba> it
[
  { _id: 'NJN', unique: 'Anthony Morrow' },
  { _id: 'NJN', unique: 'Terrence Williams' },
  { _id: 'NJN', unique: 'Keyon Dooling' },
  { _id: 'NJN', unique: 'MarShon Brooks' },
  { _id: 'NJN', unique: 'Shawne Williams' },
  { _id: 'NJN', unique: 'Trenton Hassell' },
  { _id: 'NJN', unique: 'Mehmet Okur' },
  { _id: 'NJN', unique: 'Armon Johnson' },
  { _id: 'NJN', unique: 'Gerald Green' },
  { _id: 'NJN', unique: 'Keith Bogans' },
  { _id: 'NJN', unique: 'Dennis Horner' },
  { _id: 'NJN', unique: 'Deron Williams' },
  { _id: 'NJN', unique: 'Chris Douglas-Roberts' },
  { _id: 'NJN', unique: 'Sasha Vujačić' },
  { _id: 'NJN', unique: 'Johan Petro' },
  { _id: 'NJN', unique: 'Ben Uzoh' },
  { _id: 'NJN', unique: 'Josh Boone' },
  { _id: 'NJN', unique: 'Chris Quinn' },
  { _id: 'NJN', unique: 'Derrick Favors' },
  { _id: 'NJN', unique: 'Sundiata Gaines' }
]
Type "it" for more
nba> it
[
  { _id: 'NJN', unique: 'Brook Lopez' },
  { _id: 'NJN', unique: 'Jerry Smith' },
  { _id: 'NJN', unique: 'Troy Murphy' },
  { _id: 'NJN', unique: 'Yi Jianlian' },
  { _id: 'NJN', unique: 'Brandan Wright' },
  { _id: 'NJN', unique: 'Tony Battie' },
  { _id: 'NJN', unique: 'Rafer Alston' },
  { _id: 'NJN', unique: 'Damion James' },
  { _id: 'NJN', unique: 'Orien Greene' },
  { _id: 'NJN', unique: 'Jarvis Hayes' },
  { _id: 'NJN', unique: 'Sean Williams' },
  { _id: 'NJN', unique: 'Courtney Lee' },
  { _id: 'NJN', unique: 'Dan Gadzuric' },
  { _id: 'NJN', unique: 'DeShawn Stevenson' },
  { _id: 'NJN', unique: 'Andre Emmett' },
  { _id: 'NJN', unique: 'Shelden Williams' },
  { _id: 'NJN', unique: 'Quinton Ross' },
  { _id: 'ATL', unique: 'Jeremy Tyler' },
  { _id: 'BOS', unique: 'Jaylen Brown' },
  { _id: 'BOS', unique: 'J.R. Giddens' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Chris Wilcox' },
  { _id: 'BOS', unique: 'Henry Walker' },
  { _id: 'BOS', unique: 'Jayson Tatum' },
  { _id: 'BOS', unique: 'Gerald Wallace' },
  { _id: 'BOS', unique: 'Jeff Green' },
  { _id: 'BOS', unique: 'Guerschon Yabusele' },
  { _id: 'BOS', unique: 'MarShon Brooks' },
  { _id: 'BOS', unique: 'Brian Scalabrine' },
  { _id: 'BOS', unique: 'Von Wafer' },
  { _id: 'BOS', unique: 'PJ Dozier' },
  { _id: 'BOS', unique: 'Noah Vonleh' },
  { _id: 'BOS', unique: 'Jordan Crawford' },
  { _id: 'BOS', unique: 'Robert Williams' },
  { _id: 'BOS', unique: 'Sam Hauser' },
  { _id: 'BOS', unique: 'Marquis Daniels' },
  { _id: 'BOS', unique: 'Vander Blue' },
  { _id: 'BOS', unique: 'Marcus Thornton' },
  { _id: 'BOS', unique: 'Troy Murphy' },
  { _id: 'BOS', unique: 'Mfiondu Kabengele' },
  { _id: 'BOS', unique: 'Justin Champagnie' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Ryan Hollins' },
  { _id: 'BOS', unique: 'Brandan Wright' },
  { _id: 'BOS', unique: 'Isaiah Thomas' },
  { _id: 'BOS', unique: 'Grant Williams' },
  { _id: 'BOS', unique: 'Coty Clarke' },
  { _id: 'BOS', unique: 'Juancho Hernangómez' },
  { _id: 'BOS', unique: 'Courtney Lee' },
  { _id: 'BOS', unique: 'Glen Davis' },
  { _id: 'BOS', unique: "Shaquille O'Neal" },
  { _id: 'BOS', unique: 'Demetrius Jackson' },
  { _id: 'BOS', unique: 'Jae Crowder' },
  { _id: 'BOS', unique: 'C.J. Miles' },
  { _id: 'BOS', unique: 'Kris Humphries' },
  { _id: 'BOS', unique: 'Joel Anthony' },
  { _id: 'BOS', unique: 'Kendrick Perkins' },
  { _id: 'BOS', unique: 'Abdel Nader' },
  { _id: 'BOS', unique: 'Gigi Datome' },
  { _id: 'BOS', unique: 'Terry Rozier' },
  { _id: 'BOS', unique: 'Kadeem Allen' },
  { _id: 'BOS', unique: 'Payton Pritchard' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Luke Kornet' },
  { _id: 'BOS', unique: 'Jabari Parker' },
  { _id: 'BOS', unique: 'Terrence Williams' },
  { _id: 'BOS', unique: 'Bruno Fernando' },
  { _id: 'BOS', unique: 'Justin Jackson' },
  { _id: 'BOS', unique: 'Marcus Smart' },
  { _id: 'BOS', unique: 'Greg Stiemsma' },
  { _id: 'BOS', unique: 'Mickaël Piétrus' },
  { _id: 'BOS', unique: 'Tacko Fall' },
  { _id: 'BOS', unique: 'Brodric Thomas' },
  { _id: 'BOS', unique: 'Jason Collins' },
  { _id: 'BOS', unique: 'Tristan Thompson' },
  { _id: 'BOS', unique: 'Leandro Barbosa' },
  { _id: 'BOS', unique: 'Marcus Landry' },
  { _id: 'BOS', unique: 'Delonte West' },
  { _id: 'BOS', unique: 'James Young' },
  { _id: 'BOS', unique: 'Evan Fournier' },
  { _id: 'BOS', unique: 'Semi Ojeleye' },
  { _id: 'BOS', unique: 'Malcolm Brogdon' },
  { _id: 'BOS', unique: 'Avery Bradley' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Jared Sullinger' },
  { _id: 'BOS', unique: 'Nate Robinson' },
  { _id: 'BOS', unique: 'Sean Williams' },
  { _id: 'BOS', unique: 'Phil Pressey' },
  { _id: 'BOS', unique: 'Rajon Rondo' },
  { _id: 'BOS', unique: 'Brandon Bass' },
  { _id: 'BOS', unique: 'Tony Allen' },
  { _id: 'BOS', unique: 'D.J. White' },
  { _id: 'BOS', unique: 'Oliver Lafayette' },
  { _id: 'BOS', unique: 'Darko Miličić' },
  { _id: 'BOS', unique: 'Kyrie Irving' },
  { _id: 'BOS', unique: 'Joe Johnson' },
  { _id: 'BOS', unique: 'Shane Larkin' },
  { _id: 'BOS', unique: 'JD Davison' },
  { _id: 'BOS', unique: 'Jarvis Varnado' },
  { _id: 'BOS', unique: 'Moritz Wagner' },
  { _id: 'BOS', unique: "Jermaine O'Neal" },
  { _id: 'BOS', unique: 'Eddie House' },
  { _id: 'BOS', unique: 'Al Horford' },
  { _id: 'BOS', unique: 'Keith Bogans' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Semih Erden' },
  { _id: 'BOS', unique: 'Michael Finley' },
  { _id: 'BOS', unique: 'Gerald Green' },
  { _id: 'BOS', unique: 'Jonas Jerebko' },
  { _id: 'BOS', unique: 'Jordan Mickey' },
  { _id: 'BOS', unique: 'Chris Babb' },
  { _id: 'BOS', unique: 'Romeo Langford' },
  { _id: 'BOS', unique: 'Lester Hudson' },
  { _id: 'BOS', unique: 'Mike Muscala' },
  { _id: 'BOS', unique: 'Tayshaun Prince' },
  { _id: 'BOS', unique: 'Aron Baynes' },
  { _id: 'BOS', unique: 'Greg Monroe' },
  { _id: 'BOS', unique: 'Shavlik Randolph' },
  { _id: 'BOS', unique: 'Jerryd Bayless' },
  { _id: 'BOS', unique: 'Matt Ryan' },
  { _id: 'BOS', unique: 'Blake Griffin' },
  { _id: 'BOS', unique: 'Marcus Morris' },
  { _id: 'BOS', unique: 'Evan Turner' },
  { _id: 'BOS', unique: 'Dwight Powell' },
  { _id: 'BOS', unique: "E'Twaun Moore" }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Luke Harangody' },
  { _id: 'BOS', unique: 'R.J. Hunter' },
  { _id: 'BOS', unique: 'Paul Pierce' },
  { _id: 'BOS', unique: 'Nenad Krstić' },
  { _id: 'BOS', unique: 'Aaron Nesmith' },
  { _id: 'BOS', unique: 'Kevin Garnett' },
  { _id: 'BOS', unique: 'Shelden Williams' },
  { _id: 'BOS', unique: 'Brad Wanamaker' },
  { _id: 'BOS', unique: 'Malik Fitts' },
  { _id: 'BOS', unique: 'Juwan Morgan' },
  { _id: 'BOS', unique: 'Jameer Nelson' },
  { _id: 'BOS', unique: 'JaJuan Johnson' },
  { _id: 'BOS', unique: 'Gordon Hayward' },
  { _id: 'BOS', unique: 'Tremont Waters' },
  { _id: 'BOS', unique: 'Rasheed Wallace' },
  { _id: 'BOS', unique: 'Jason Terry' },
  { _id: 'BOS', unique: 'Amir Johnson' },
  { _id: 'BOS', unique: 'Kris Joseph' },
  { _id: 'BOS', unique: 'David Lee' },
  { _id: 'BOS', unique: 'Jarell Eddie' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Daniel Theis' },
  { _id: 'BOS', unique: 'Ray Allen' },
  { _id: 'BOS', unique: 'Keyon Dooling' },
  { _id: 'BOS', unique: 'Carsen Edwards' },
  { _id: 'BOS', unique: 'Jeff Teague' },
  { _id: 'BOS', unique: 'Vítor Luiz Faverani' },
  { _id: 'BOS', unique: 'Carlos Arroyo' },
  { _id: 'BOS', unique: 'Dennis Schröder' },
  { _id: 'BOS', unique: 'Tyler Zeller' },
  { _id: 'BOS', unique: 'Javonte Green' },
  { _id: 'BOS', unique: 'Kelly Olynyk' },
  { _id: 'BOS', unique: 'Kemba Walker' },
  { _id: 'BOS', unique: 'Jabari Bird' },
  { _id: 'BOS', unique: 'Kelan Martin' },
  { _id: 'BOS', unique: 'Enes Freedom' },
  { _id: 'BOS', unique: 'Nik Stauskas' },
  { _id: 'BOS', unique: 'Chris Johnson' },
  { _id: 'BOS', unique: 'Xavier Silas' },
  { _id: 'BOS', unique: 'Vincent Poirier' },
  { _id: 'BOS', unique: 'Jonathan Gibson' }
]
Type "it" for more
nba> it
[
  { _id: 'BOS', unique: 'Josh Richardson' },
  { _id: 'BOS', unique: 'Fab Melo' },
  { _id: 'BOS', unique: 'Sasha Pavlović' },
  { _id: 'BOS', unique: 'Derrick White' },
  { _id: 'PHI', unique: 'JaVale McGee' },
  { _id: 'PHI', unique: 'Justin Anderson' },
  { _id: 'PHI', unique: "De'Anthony Melton" },
  { _id: 'PHI', unique: 'Malcolm Thomas' },
  { _id: 'PHI', unique: 'Dorell Wright' },
  { _id: 'PHI', unique: 'Lou Williams' },
  { _id: 'PHI', unique: 'Georges Niang' },
  { _id: 'PHI', unique: 'Thaddeus Young' },
  { _id: 'PHI', unique: 'Dwight Howard' },
  { _id: 'PHI', unique: 'Ignas Brazdeikis' },
  { _id: 'PHI', unique: 'Timothé Luwawu-Cabarrot' },
  { _id: 'PHI', unique: 'Alexey Shved' },
  { _id: 'PHI', unique: 'James Harden' },
  { _id: 'PHI', unique: 'Kendall Marshall' },
  { _id: 'PHI', unique: 'Dewayne Dedmon' },
  { _id: 'PHI', unique: 'Justin Holiday' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Thomas Robinson' },
  { _id: 'PHI', unique: 'Ben Simmons' },
  { _id: 'PHI', unique: 'Primož Brezec' },
  { _id: 'PHI', unique: 'Jonathon Simmons' },
  { _id: 'PHI', unique: 'Tyler Johnson' },
  { _id: 'PHI', unique: 'Jrue Holiday' },
  { _id: 'PHI', unique: 'Marreese Speights' },
  { _id: 'PHI', unique: 'Zhaire Smith' },
  { _id: 'PHI', unique: 'Andre Iguodala' },
  { _id: 'PHI', unique: 'Darius Johnson-Odom' },
  { _id: 'PHI', unique: 'Danuel House Jr.' },
  { _id: 'PHI', unique: 'Alex Poythress' },
  { _id: 'PHI', unique: 'Seth Curry' },
  { _id: 'PHI', unique: 'Hollis Thompson' },
  { _id: 'PHI', unique: 'Michael Foster Jr.' },
  { _id: 'PHI', unique: 'Byron Mullens' },
  { _id: 'PHI', unique: 'Drew Gordon' },
  { _id: 'PHI', unique: 'Paul Millsap' },
  { _id: 'PHI', unique: 'DeAndre Jordan' },
  { _id: 'PHI', unique: 'Shawn Long' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Demetrius Jackson' },
  { _id: 'PHI', unique: 'Samuel Dalembert' },
  { _id: 'PHI', unique: 'Arnett Moultrie' },
  { _id: 'PHI', unique: 'Jeremy Pargo' },
  { _id: 'PHI', unique: 'Jaden Springer' },
  { _id: 'PHI', unique: 'Terrance Ferguson' },
  { _id: 'PHI', unique: 'Lavoy Allen' },
  { _id: 'PHI', unique: 'Haywood Highsmith' },
  { _id: 'PHI', unique: 'Ersan İlyasova' },
  { _id: 'PHI', unique: 'Louis King' },
  { _id: 'PHI', unique: 'Trey Burke' },
  { _id: 'PHI', unique: 'Isaiah Canaan' },
  { _id: 'PHI', unique: 'Mac McClung' },
  { _id: 'PHI', unique: 'Jason Smith' },
  { _id: 'PHI', unique: 'Michael Carter-Williams' },
  { _id: 'PHI', unique: 'Ish Smith' },
  { _id: 'PHI', unique: 'Damien Wilkins' },
  { _id: 'PHI', unique: 'JaKarr Sampson' },
  { _id: 'PHI', unique: 'Joel Embiid' },
  { _id: 'PHI', unique: 'Carl Landry' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Andrés Nocioni' },
  { _id: 'PHI', unique: 'Willie Cauley-Stein' },
  { _id: 'PHI', unique: 'Royal Ivey' },
  { _id: 'PHI', unique: 'Aaron Henry' },
  { _id: 'PHI', unique: 'Jerami Grant' },
  { _id: 'PHI', unique: 'Francisco Elson' },
  { _id: 'PHI', unique: 'Justin Harper' },
  { _id: 'PHI', unique: 'Darius Songaila' },
  { _id: 'PHI', unique: 'Marco Belinelli' },
  { _id: 'PHI', unique: 'James Young' },
  { _id: 'PHI', unique: 'Antonio Daniels' },
  { _id: 'PHI', unique: 'Shelvin Mack' },
  { _id: 'PHI', unique: 'Darius Morris' },
  { _id: 'PHI', unique: 'Corey Brewer' },
  { _id: 'PHI', unique: 'Rayjon Tucker' },
  { _id: 'PHI', unique: 'Myles Powell' },
  { _id: 'PHI', unique: 'Jalen McDaniels' },
  { _id: 'PHI', unique: 'Willie Green' },
  { _id: 'PHI', unique: 'Shake Milton' },
  { _id: 'PHI', unique: 'James Michael McAdoo' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Norvel Pelle' },
  { _id: 'PHI', unique: 'Phil Pressey' },
  { _id: 'PHI', unique: 'Elton Brand' },
  { _id: 'PHI', unique: 'Sam Young' },
  { _id: 'PHI', unique: 'Landry Shamet' },
  { _id: 'PHI', unique: 'Alec Burks' },
  { _id: 'PHI', unique: 'Jarvis Varnado' },
  { _id: 'PHI', unique: 'Anthony Tolliver' },
  { _id: 'PHI', unique: 'Furkan Korkmaz' },
  { _id: 'PHI', unique: 'Montrezl Harrell' },
  { _id: 'PHI', unique: 'Nick Young' },
  { _id: 'PHI', unique: 'Daniel Orton' },
  { _id: 'PHI', unique: 'Allen Iverson' },
  { _id: 'PHI', unique: 'Dario Šarić' },
  { _id: 'PHI', unique: 'Jacob Pullen' },
  { _id: 'PHI', unique: 'Al Horford' },
  { _id: 'PHI', unique: 'Rodney Carney' },
  { _id: 'PHI', unique: 'Spencer Hawes' },
  { _id: 'PHI', unique: 'Andre Drummond' },
  { _id: 'PHI', unique: 'Jason Richardson' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Tony Wroten' },
  { _id: 'PHI', unique: 'Danny Green' },
  { _id: 'PHI', unique: 'Gary Clark' },
  { _id: 'PHI', unique: 'J.J. Redick' },
  { _id: 'PHI', unique: 'Nerlens Noel' },
  { _id: 'PHI', unique: 'Matisse Thybulle' },
  { _id: 'PHI', unique: 'Wilson Chandler' },
  { _id: 'PHI', unique: 'Mike Muscala' },
  { _id: 'PHI', unique: 'Casper Ware' },
  { _id: 'PHI', unique: 'Marial Shayok' },
  { _id: 'PHI', unique: 'T.J. McConnell' },
  { _id: 'PHI', unique: 'Greg Monroe' },
  { _id: 'PHI', unique: 'Markelle Fultz' },
  { _id: 'PHI', unique: 'Jerryd Bayless' },
  { _id: 'PHI', unique: 'George Hill' },
  { _id: 'PHI', unique: 'Paul Reed' },
  { _id: 'PHI', unique: 'Lorenzo Brown' },
  { _id: 'PHI', unique: 'Mike Scott' },
  { _id: 'PHI', unique: 'Evan Turner' },
  { _id: 'PHI', unique: 'Christian Wood' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Jason Kapono' },
  { _id: 'PHI', unique: 'Charles Jenkins' },
  { _id: 'PHI', unique: 'K.J. McDaniels' },
  { _id: 'PHI', unique: 'Mason Jones' },
  { _id: 'PHI', unique: 'Isaiah Joe' },
  { _id: 'PHI', unique: 'Trevor Booker' },
  { _id: 'PHI', unique: 'Charles Bassey' },
  { _id: 'PHI', unique: 'P.J. Tucker' },
  { _id: 'PHI', unique: 'Braxton Key' },
  { _id: 'PHI', unique: 'Elliot Williams' },
  { _id: 'PHI', unique: 'Tobias Harris' },
  { _id: 'PHI', unique: 'Brandon Davies' },
  { _id: 'PHI', unique: 'Raul Neto' },
  { _id: 'PHI', unique: 'Kwame Brown' },
  { _id: 'PHI', unique: 'Nikola Vučević' },
  { _id: 'PHI', unique: "Kyle O'Quinn" },
  { _id: 'PHI', unique: 'Maalik Wayns' },
  { _id: 'PHI', unique: 'Tiago Splitter' },
  { _id: 'PHI', unique: 'Jonah Bolden' },
  { _id: 'PHI', unique: 'Tony Bradley' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Gerald Henderson' },
  { _id: 'PHI', unique: 'Dakota Mathias' },
  { _id: 'PHI', unique: 'Amir Johnson' },
  { _id: 'PHI', unique: 'Justin Patton' },
  { _id: 'PHI', unique: 'Robert Covington' },
  { _id: 'PHI', unique: 'Glenn Robinson III' },
  { _id: 'PHI', unique: 'Boban Marjanović' },
  { _id: 'PHI', unique: 'Jahlil Okafor' },
  { _id: 'PHI', unique: 'Sergio Rodríguez' },
  { _id: 'PHI', unique: 'Larry Drew II' },
  { _id: 'PHI', unique: 'Jimmy Butler' },
  { _id: 'PHI', unique: 'Furkan Aldemir' },
  { _id: 'PHI', unique: 'Tyrese Maxey' },
  { _id: 'PHI', unique: 'James Ennis III' },
  { _id: 'PHI', unique: 'Julian Champagnie' },
  { _id: 'PHI', unique: 'Henry Sims' },
  { _id: 'PHI', unique: 'Charlie Brown Jr.' },
  { _id: 'PHI', unique: 'Saben Lee' },
  { _id: 'PHI', unique: 'Nik Stauskas' },
  { _id: 'PHI', unique: 'Jodie Meeks' }
]
Type "it" for more
nba> it
[
  { _id: 'PHI', unique: 'Tony Battie' },
  { _id: 'PHI', unique: 'Craig Brackins' },
  { _id: 'PHI', unique: 'Tim Frazier' },
  { _id: 'PHI', unique: 'Xavier Silas' },
  { _id: 'PHI', unique: 'Chasson Randle' },
  { _id: 'PHI', unique: 'Luc Mbah a Moute' },
  { _id: 'PHI', unique: 'Chris Johnson' },
  { _id: 'PHI', unique: 'Vincent Poirier' },
  { _id: 'PHI', unique: 'Eric Maynor' },
  { _id: 'PHI', unique: 'Malcolm Lee' },
  { _id: 'PHI', unique: 'Richaun Holmes' },
  { _id: 'PHI', unique: 'James Anderson' },
  { _id: 'PHI', unique: 'Sonny Weems' },
  { _id: 'PHI', unique: 'Adonis Thomas' },
  { _id: 'PHI', unique: 'James Nunnally' },
  { _id: 'PHI', unique: 'Josh Richardson' },
  { _id: 'NYK', unique: 'Chris Duhon' },
  { _id: 'NYK', unique: 'Mindaugas Kuzminskas' },
  { _id: 'NYK', unique: 'J.R. Giddens' },
  { _id: 'NYK', unique: 'Carmelo Anthony' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Henry Walker' },
  { _id: 'NYK', unique: 'Julius Randle' },
  { _id: 'NYK', unique: 'Bobby Portis' },
  { _id: 'NYK', unique: 'Ignas Brazdeikis' },
  { _id: 'NYK', unique: 'Jerome Jordan' },
  { _id: 'NYK', unique: 'Quincy Acy' },
  { _id: 'NYK', unique: 'Frank Ntilikina' },
  { _id: 'NYK', unique: 'Alexey Shved' },
  { _id: 'NYK', unique: 'Feron Hunt' },
  { _id: 'NYK', unique: 'Tyler Hall' },
  { _id: 'NYK', unique: 'Maurice Ndour' },
  { _id: 'NYK', unique: 'Noah Vonleh' },
  { _id: 'NYK', unique: 'Steve Novak' },
  { _id: 'NYK', unique: 'Marcus Camby' },
  { _id: 'NYK', unique: 'Justin Holiday' },
  { _id: 'NYK', unique: 'Beno Udrih' },
  { _id: 'NYK', unique: 'J.R. Smith' },
  { _id: 'NYK', unique: 'Pablo Prigioni' },
  { _id: 'NYK', unique: 'Thanasis Antetokounmpo' },
  { _id: 'NYK', unique: 'Josh Harrellson' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Sasha Vujačić' },
  { _id: 'NYK', unique: 'Quentin Grimes' },
  { _id: 'NYK', unique: 'Andy Rautins' },
  { _id: 'NYK', unique: 'Danuel House Jr.' },
  { _id: 'NYK', unique: 'Isaiah Hartenstein' },
  { _id: 'NYK', unique: 'Jason Kidd' },
  { _id: 'NYK', unique: 'Al Harrington' },
  { _id: 'NYK', unique: 'Kevin Séraphin' },
  { _id: 'NYK', unique: 'Metta World Peace' },
  { _id: 'NYK', unique: 'Travis Wear' },
  { _id: 'NYK', unique: 'Jarrett Jack' },
  { _id: 'NYK', unique: 'DeAndre Jordan' },
  { _id: 'NYK', unique: 'Reggie Bullock' },
  { _id: 'NYK', unique: 'Austin Rivers' },
  { _id: 'NYK', unique: 'Toney Douglas' },
  { _id: 'NYK', unique: 'Courtney Lee' },
  { _id: 'NYK', unique: 'Ryan Arcidiacono' },
  { _id: 'NYK', unique: 'Jonathan Bender' },
  { _id: 'NYK', unique: 'Immanuel Quickley' },
  { _id: 'NYK', unique: 'Michael Beasley' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Samuel Dalembert' },
  { _id: 'NYK', unique: 'Jared Jeffries' },
  { _id: 'NYK', unique: 'Cole Aldrich' },
  { _id: 'NYK', unique: 'Kadeem Allen' },
  { _id: 'NYK', unique: 'Henry Ellenson' },
  { _id: 'NYK', unique: 'Tyson Chandler' },
  { _id: 'NYK', unique: 'Robin Lopez' },
  { _id: 'NYK', unique: 'Earl Barron' },
  { _id: 'NYK', unique: 'Brandon Jennings' },
  { _id: 'NYK', unique: 'Luke Kornet' },
  { _id: 'NYK', unique: 'Trey Burke' },
  { _id: 'NYK', unique: 'Jason Smith' },
  { _id: 'NYK', unique: 'John Jenkins' },
  { _id: 'NYK', unique: 'Derrick Rose' },
  { _id: 'NYK', unique: 'Troy Williams' },
  { _id: 'NYK', unique: 'Josh Hart' },
  { _id: 'NYK', unique: 'Chris Copeland' },
  { _id: 'NYK', unique: "Amar'e Stoudemire" },
  { _id: 'NYK', unique: 'Ronny Turiaf' },
  { _id: 'NYK', unique: 'Marshall Plumlee' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Obi Toppin' },
  { _id: 'NYK', unique: 'Wesley Matthews' },
  { _id: 'NYK', unique: 'Andrea Bargnani' },
  { _id: 'NYK', unique: 'RJ Barrett' },
  { _id: 'NYK', unique: 'Jeremy Lin' },
  { _id: 'NYK', unique: 'Marcus Landry' },
  { _id: 'NYK', unique: 'Kristaps Porziņģis' },
  { _id: 'NYK', unique: 'Evan Fournier' },
  { _id: 'NYK', unique: 'Doug McDermott' },
  { _id: 'NYK', unique: 'Jericho Sims' },
  { _id: 'NYK', unique: 'Nate Robinson' },
  { _id: 'NYK', unique: 'Roger Mason' },
  { _id: 'NYK', unique: 'Billy Garrett' },
  { _id: 'NYK', unique: 'Norvel Pelle' },
  { _id: 'NYK', unique: 'Jalen Brunson' },
  { _id: 'NYK', unique: 'Miles McBride' },
  { _id: 'NYK', unique: 'Darko Miličić' },
  { _id: 'NYK', unique: 'Elfrid Payton' },
  { _id: 'NYK', unique: 'Shane Larkin' },
  { _id: 'NYK', unique: 'Alec Burks' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Mario Hezonja' },
  { _id: 'NYK', unique: 'José Calderón' },
  { _id: 'NYK', unique: 'Emmanuel Mudiay' },
  { _id: 'NYK', unique: 'Damyean Dotson' },
  { _id: 'NYK', unique: 'Kurt Thomas' },
  { _id: 'NYK', unique: 'Eddie House' },
  { _id: 'NYK', unique: 'Iman Shumpert' },
  { _id: 'NYK', unique: 'Danilo Gallinari' },
  { _id: 'NYK', unique: 'Shawne Williams' },
  { _id: 'NYK', unique: 'Timofey Mozgov' },
  { _id: 'NYK', unique: 'Raymond Felton' },
  { _id: 'NYK', unique: 'Ronnie Brewer' },
  { _id: 'NYK', unique: 'Chris Smith' },
  { _id: 'NYK', unique: 'Lou Amundson' },
  { _id: 'NYK', unique: 'Nerlens Noel' },
  { _id: 'NYK', unique: 'Wilson Chandler' },
  { _id: 'NYK', unique: 'Kenyon Martin' },
  { _id: 'NYK', unique: 'Dennis Smith Jr.' },
  { _id: 'NYK', unique: 'Langston Galloway' },
  { _id: 'NYK', unique: 'Anthony Randolph' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Isaiah Hicks' },
  { _id: 'NYK', unique: 'Tracy McGrady' },
  { _id: 'NYK', unique: 'Allonzo Trier' },
  { _id: 'NYK', unique: 'Theo Pinson' },
  { _id: 'NYK', unique: 'Anthony Carter' },
  { _id: 'NYK', unique: 'Earl Clark' },
  { _id: 'NYK', unique: 'Matt Mooney' },
  { _id: 'NYK', unique: 'Joakim Noah' },
  { _id: 'NYK', unique: 'Mike Bibby' },
  { _id: 'NYK', unique: "Toure' Murry" },
  { _id: 'NYK', unique: 'Shannon Brown' },
  { _id: 'NYK', unique: 'Marcus Morris' },
  { _id: 'NYK', unique: 'Maurice Harkless' },
  { _id: 'NYK', unique: 'Arron Afflalo' },
  { _id: 'NYK', unique: 'Ron Baker' },
  { _id: 'NYK', unique: 'Jordan Hill' },
  { _id: 'NYK', unique: 'Shelden Williams' },
  { _id: 'NYK', unique: 'Willy Hernangómez' },
  { _id: 'NYK', unique: 'Larry Hughes' },
  { _id: 'NYK', unique: 'Renaldo Balkman' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Derrick Brown' },
  { _id: 'NYK', unique: 'Jimmer Fredette' },
  { _id: 'NYK', unique: 'Lance Thomas' },
  { _id: 'NYK', unique: "Kyle O'Quinn" },
  { _id: 'NYK', unique: 'Jared Harper' },
  { _id: 'NYK', unique: 'Tim Hardaway Jr.' },
  { _id: 'NYK', unique: 'Svi Mykhailiuk' },
  { _id: 'NYK', unique: 'Kevin Knox' },
  { _id: 'NYK', unique: 'Rasheed Wallace' },
  { _id: 'NYK', unique: 'James White' },
  { _id: 'NYK', unique: 'David Lee' },
  { _id: 'NYK', unique: 'Landry Fields' },
  { _id: 'NYK', unique: 'Sergio Rodríguez' },
  { _id: 'NYK', unique: 'Wayne Ellington' },
  { _id: 'NYK', unique: 'Eddy Curry' },
  { _id: 'NYK', unique: 'Baron Davis' },
  { _id: 'NYK', unique: 'Mitchell Robinson' },
  { _id: 'NYK', unique: 'Ricky Ledo' },
  { _id: 'NYK', unique: 'Jerian Grant' },
  { _id: 'NYK', unique: 'Kemba Walker' }
]
Type "it" for more
nba> it
[
  { _id: 'NYK', unique: 'Wayne Selden' },
  { _id: 'NYK', unique: 'Enes Freedom' },
  { _id: 'NYK', unique: 'Jeremy Tyler' },
  { _id: 'NYK', unique: 'Trevor Keels' },
  { _id: 'NYK', unique: 'Quentin Richardson' },
  { _id: 'NYK', unique: 'Derrick Williams' },
  { _id: 'NYK', unique: 'Chasson Randle' },
  { _id: 'NYK', unique: 'Solomon Jones' },
  { _id: 'NYK', unique: 'Cleanthony Early' },
  { _id: 'NYK', unique: 'Ramon Sessions' },
  { _id: 'NYK', unique: 'Cam Reddish' },
  { _id: 'NYK', unique: 'Dan Gadzuric' },
  { _id: 'NYK', unique: 'Taj Gibson' },
  { _id: 'NYK', unique: 'Chauncey Billups' },
  { _id: 'MEM', unique: 'Brian Skinner' }
]






'''
