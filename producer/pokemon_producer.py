import json
import time
import random
import requests
import logging
from kafka import KafkaProducer
from datetime import datetime
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokemonProducer:
    def __init__(self):
        self.kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        self.topic = os.getenv('KAFKA_TOPIC', 'pokemon-data')
        
        # Crear productor de Kafka
        self.producer = KafkaProducer(
            bootstrap_servers=[self.kafka_servers],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            key_serializer=lambda x: x.encode('utf-8') if x else None,
            retries=5,
            retry_backoff_ms=100
        )
        
        logger.info(f"Productor inicializado: {self.kafka_servers}, topic: {self.topic}")

    def fetch_pokemon_data(self, pokemon_id):
        """Obtener datos de un Pokemon desde la PokeAPI"""
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extraer información relevante
            pokemon_data = {
                'id': data['id'],
                'name': data['name'],
                'height': data['height'],
                'weight': data['weight'],
                'base_experience': data['base_experience'],
                'types': [t['type']['name'] for t in data['types']],
                'abilities': [a['ability']['name'] for a in data['abilities']],
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                'timestamp': datetime.now().isoformat()
            }
            
            return pokemon_data
            
        except Exception as e:
            logger.error(f"Error obteniendo Pokemon {pokemon_id}: {e}")
            return None

    def send_pokemon_data(self, pokemon_data):
        """Enviar datos de Pokemon a Kafka"""
        try:
            key = str(pokemon_data['id'])
            
            future = self.producer.send(
                self.topic, 
                key=key,
                value=pokemon_data
            )
            
            # Esperar confirmación
            record_metadata = future.get(timeout=10)
            
            logger.info(f"Pokemon {pokemon_data['name']} enviado - Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
            
        except Exception as e:
            logger.error(f"Error enviando datos: {e}")

    def run(self):
        """Ejecutar el productor"""
        logger.info("Iniciando productor de Pokemon...")
        
        # IDs de Pokemon para obtener (primeros 150 Pokemon originales)
        pokemon_ids = list(range(1, 151))
        
        try:
            while True:
                # Seleccionar Pokemon aleatorio
                pokemon_id = random.choice(pokemon_ids)
                
                # Obtener datos del Pokemon
                pokemon_data = self.fetch_pokemon_data(pokemon_id)
                
                if pokemon_data:
                    # Enviar a Kafka
                    self.send_pokemon_data(pokemon_data)
                else:
                    logger.warning(f"No se pudieron obtener datos para Pokemon {pokemon_id}")
                
                # Esperar antes del siguiente envío (3-8 segundos)
                time.sleep(random.uniform(3, 8))
                
        except KeyboardInterrupt:
            logger.info("Deteniendo productor...")
        finally:
            self.producer.close()

if __name__ == "__main__":
    producer = PokemonProducer()
    producer.run()