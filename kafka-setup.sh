#!/bin/bash

echo "Esperando a que Kafka esté listo..."
sleep 10

echo "Creando topic pokemon-data..."
docker exec kafka kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 3 \
    --topic pokemon-data

echo "Listando topics..."
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

echo "Setup de Kafka completado!"
