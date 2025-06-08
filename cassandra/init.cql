-- Crear keyspace para Pokemon
CREATE KEYSPACE IF NOT EXISTS pokemon_data 
WITH replication = {
  'class': 'SimpleStrategy', 
  'replication_factor': 1
};

USE pokemon_data;

-- Tabla para datos raw de Pokemon
CREATE TABLE IF NOT EXISTS raw_pokemon (
    id int,
    name text,
    height int,
    weight int,
    base_experience int,
    types list<text>,
    abilities list<text>,
    stats map<text, int>,
    timestamp timestamp,
    PRIMARY KEY (id)
);

-- Tabla para estadísticas agregadas
CREATE TABLE IF NOT EXISTS pokemon_stats (
    stat_type text,
    avg_value double,
    max_value int,
    min_value int,
    count_pokemon bigint,
    updated_at timestamp,
    PRIMARY KEY (stat_type)
);

-- Tabla para Pokemon por tipo
CREATE TABLE IF NOT EXISTS pokemon_by_type (
    type text,
    pokemon_id int,
    pokemon_name text,
    base_experience int,
    timestamp timestamp,
    PRIMARY KEY (type, pokemon_id)
);