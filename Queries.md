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
