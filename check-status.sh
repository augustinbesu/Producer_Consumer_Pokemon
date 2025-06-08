#!/bin/bash

echo "=== Estado de los contenedores ==="
docker-compose ps

echo ""
echo "=== Verificando Kafka ==="
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092 2>/dev/null || echo "Kafka no está listo"

echo ""
echo "=== Verificando Cassandra ==="
docker exec cassandra cqlsh -e "USE pokemon_data; DESCRIBE TABLES;" 2>/dev/null || echo "Cassandra no está listo"

echo ""
echo "=== URLs de acceso ==="
echo "Spark Master: http://localhost:8080"
echo "Spark Worker: http://localhost:8081"
echo "Jupyter Lab: http://localhost:8888 (token: pokemon123)"
echo "Kafka: localhost:29092"
echo "Cassandra: localhost:9042"