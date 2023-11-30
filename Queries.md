# Mongo

## Consulta para identificar jugadores con un alto porcentaje de tiros de campo y una participación activa en la temporada, esencial para evaluar la consistencia y eficacia en jugadores clave.

```
collection.find({
    "field_percent": { "$gt": "0.550" },
    "games": { "$gt": 50 }
}).sort("field_percent", -1).limit(15)
```

## Consulta que destaca a los jugadores con el mayor número de asistencias en la temporada 2010, crucial para entender quiénes son los mejores facilitadores en el juego.

```
collection.aggregate([
    { "$match": { "season": 2010 } },
    { "$group": { "_id": "$player_name", "totalAssists": { "$sum": "$AST" } } },
    { "$sort": { "totalAssists": -1 } },
    { "$limit": 7 }
])
```

## Consulta que identifica al jugador con mejor promedio en tiros de tres puntos por temporada, proporcionando insights sobre los tiradores más eficientes año tras año.

```
collection.aggregate([
    { "$unwind": "$season" },
    { "$group": { "_id": { "player": "$player_name", "season": "$season" }, "avgThreePoints": { "$avg": "$three_percent" } } },
    { "$sort": { "_id.season": 1, "avgThreePoints": -1 } },
    { "$group": { "_id": "$_id.season", "bestThreePointPlayer": { "$first": "$_id.player" } } },
    { "$sort": { "_id": 1 } }
])
```

# Cassandra

## Consulta para Encontrar Jugadores con la Mayor Cantidad de Asistencias y Robos en una Temporada

```
SELECT player_name, season, AST, STL
FROM player_stats
WHERE AST > 500 AND STL > 100
ALLOW FILTERING;
```

## Consulta para Encontrar Jugadores con Alto Rendimiento en Tiros de Campo

```
SELECT player_name, season, team, field_percent, field_attempts
FROM player_stats
WHERE field_percent >= '0.500' AND field_attempts > 500
ALLOW FILTERING;
```

## Consulta para Jugadores con Alto Impacto Defensivo

```
SELECT player_name, season, team, DRB, BLK
FROM player_stats
WHERE DRB > 300 AND BLK > 50
ALLOW FILTERING;
```

# Neo4j

## 
