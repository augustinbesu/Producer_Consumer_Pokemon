import json
import logging
from kafka import KafkaConsumer
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokemonConsumer:
    def __init__(self):
        self.kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        self.topic = os.getenv('KAFKA_TOPIC', 'pokemon-data')
        
        # Crear consumidor de Kafka
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=[self.kafka_servers],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='pokemon-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        logger.info(f"Consumidor inicializado: {self.kafka_servers}, topic: {self.topic}")

    def run(self):
        """Ejecutar el consumidor"""
        logger.info("Iniciando consumidor de Pokemon...")
        
        try:
            for message in self.consumer:
                pokemon_data = message.value
                
                logger.info(f"Pokemon recibido: {pokemon_data['name']} (ID: {pokemon_data['id']})")
                logger.info(f"  - Tipos: {', '.join(pokemon_data['types'])}")
                logger.info(f"  - Altura: {pokemon_data['height']}, Peso: {pokemon_data['weight']}")
                logger.info(f"  - Experiencia base: {pokemon_data['base_experience']}")
                logger.info(f"  - Timestamp: {pokemon_data['timestamp']}")
                logger.info("-" * 50)
                
        except KeyboardInterrupt:
            logger.info("Deteniendo consumidor...")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    consumer = PokemonConsumer()
    consumer.run()