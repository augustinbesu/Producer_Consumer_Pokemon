.PHONY: build up down logs clean setup status check-cassandra logs-producer logs-consumer logs-spark restart-producer restart-consumer restart-spark

# Construir todas las imágenes
build:
	docker compose build

# Levantar todos los servicios
up:
	docker compose up -d

# Parar todos los servicios
down:
	docker compose down

# Ver logs de todos los servicios
logs:
	docker compose logs -f

# Limpiar todo (contenedores, imágenes, volúmenes)
clean:
	docker compose down -v
	docker system prune -af

# Setup completo
setup: build up
	@echo "Esperando a que los servicios estén listos..."
	@sleep 30
	@echo "Configurando Kafka..."
	@chmod +x kafka-setup.sh
	@./kafka-setup.sh
	@echo "¡Setup completado!"
	@echo ""
	@echo "Servicios disponibles:"
	@echo "- Spark Master UI: http://localhost:8080"
	@echo "- Jupyter Lab: http://localhost:8888 (token: pokemon123)"
	@echo "- Grafana: http://localhost:3000 (admin/pokemon123)"
	@echo "- Kafka: localhost:29092"
	@echo "- Cassandra: localhost:9042"

# Ver estado de los servicios
status:
	docker compose ps

# Verificar datos en Cassandra
check-cassandra:
	docker exec cassandra cqlsh -e "USE pokemon_data; SELECT COUNT(*) FROM raw_pokemon;"
	docker exec cassandra cqlsh -e "USE pokemon_data; SELECT * FROM pokemon_stats;"

# Ver logs específicos
logs-producer:
	docker compose logs -f pokemon-producer

logs-consumer:
	docker compose logs -f pokemon-consumer

logs-spark:
	docker compose logs -f spark-processor

logs-grafana:
	docker compose logs -f grafana

# Reiniciar servicios específicos
restart-producer:
	docker compose restart pokemon-producer

restart-consumer:
	docker compose restart pokemon-consumer

restart-spark:
	docker compose restart spark-processor

restart-grafana:
	docker compose restart grafana
