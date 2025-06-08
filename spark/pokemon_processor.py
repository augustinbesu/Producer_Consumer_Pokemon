import os
import logging 
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokemonSparkProcessor:
    def __init__(self):
        self.spark_master = os.getenv('SPARK_MASTER_URL', 'local[2]')
        self.kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
        self.cassandra_host = os.getenv('CASSANDRA_HOST', 'localhost')
        
        # Crear sesión de Spark con configuración mejorada
        self.spark = SparkSession.builder \
            .appName("PokemonProcessor") \
            .master(self.spark_master) \
            .config("spark.cassandra.connection.host", self.cassandra_host) \
            .config("spark.cassandra.connection.port", "9042") \
            .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
            .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
            .config("spark.cassandra.connection.timeoutMS", "60000") \
            .config("spark.cassandra.connection.reconnectionDelayMS.max", "30000") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .config("spark.kryo.registrationRequired", "false") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info("Spark session creada con extensiones de Cassandra")
        
        # Verificar conexión a Cassandra
        self.verify_cassandra_connection()

    def verify_cassandra_connection(self):
        """Verificar que Cassandra esté accesible"""
        try:
            # Intentar leer de una tabla conocida
            test_df = self.spark.read \
                .format("org.apache.spark.sql.cassandra") \
                .option("keyspace", "pokemon_data") \
                .option("table", "raw_pokemon") \
                .load()
            
            # Solo contar sin mostrar datos
            count = test_df.count()
            logger.info(f"Conexión a Cassandra verificada. Registros existentes: {count}")
            
        except Exception as e:
            logger.warning(f"No se pudo verificar conexión a Cassandra: {e}")
            logger.info("Continuando... la tabla puede no existir aún")

    def create_kafka_stream(self):
        """Crear stream de Kafka"""
        return self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_servers) \
            .option("subscribe", "pokemon-data") \
            .option("startingOffsets", "latest") \
            .option("failOnDataLoss", "false") \
            .load()

    def debug_kafka_data(self, df, epoch_id):
        """Debug: mostrar datos raw de Kafka"""
        try:
            logger.info(f"=== DEBUG BATCH {epoch_id} ===")
            
            # Contar registros usando cache para mejorar rendimiento
            df.cache()
            count = df.count()
            logger.info(f"Total registros en batch: {count}")
            
            if count > 0:
                # Mostrar algunas muestras
                sample_rows = df.select(col("value").cast("string")).limit(3).collect()
                for i, row in enumerate(sample_rows):
                    logger.info(f"Registro {i}: {row['value'][:100]}...")
            
            df.unpersist()  # Limpiar cache
            
        except Exception as e:
            logger.error(f"Error en debug: {e}")

    def process_pokemon_data(self, df):
        """Procesar datos de Pokemon"""
        try:
            # Convertir datos de Kafka a string
            string_df = df.select(col("value").cast("string").alias("json_data"))
            
            # Schema para Pokemon
            pokemon_schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("name", StringType(), True),
                StructField("height", IntegerType(), True),
                StructField("weight", IntegerType(), True),
                StructField("base_experience", IntegerType(), True),
                StructField("types", ArrayType(StringType()), True),
                StructField("abilities", ArrayType(StringType()), True),
                StructField("stats", MapType(StringType(), IntegerType()), True),
                StructField("timestamp", StringType(), True)
            ])
            
            # Parsear JSON
            parsed_df = string_df.select(
                from_json(col("json_data"), pokemon_schema).alias("pokemon")
            ).select("pokemon.*")
            
            # Filtrar registros válidos y convertir timestamp
            processed_df = parsed_df.filter(col("id").isNotNull()) \
                .withColumn("timestamp", to_timestamp(col("timestamp")))
            
            return processed_df
            
        except Exception as e:
            logger.error(f"Error procesando datos: {e}")
            return self.spark.createDataFrame([], schema=StructType([]))

    def write_to_cassandra_raw(self, df, epoch_id):
        """Escribir datos raw a Cassandra"""
        try:
            # Cache para mejorar rendimiento
            df.cache()
            count = df.count()
            
            if count == 0:
                logger.info(f"Batch {epoch_id}: No hay datos para escribir")
                df.unpersist()
                return
            
            logger.info(f"Batch {epoch_id}: Escribiendo {count} registros a Cassandra...")
            
            # Escribir directamente sin recrear DataFrame
            df.write \
                .format("org.apache.spark.sql.cassandra") \
                .option("keyspace", "pokemon_data") \
                .option("table", "raw_pokemon") \
                .mode("append") \
                .save()
            
            logger.info(f"Batch {epoch_id}: {count} registros escritos a raw_pokemon")
            df.unpersist()
            
        except Exception as e:
            logger.error(f"Error escribiendo a Cassandra: {e}")
            if hasattr(df, 'unpersist'):
                df.unpersist()

    def write_pokemon_stats(self, df, epoch_id):
        """Escribir estadísticas agregadas"""
        try:
            df.cache()
            count = df.count()
            
            if count == 0:
                df.unpersist()
                return
            
            # Calcular estadísticas por tipo
            from pyspark.sql.functions import avg, max as spark_max, min as spark_min, count as spark_count
            
            # Estadísticas de experiencia base
            exp_stats = df.agg(
                avg("base_experience").alias("avg_exp"),
                spark_max("base_experience").alias("max_exp"),
                spark_min("base_experience").alias("min_exp"),
                spark_count("base_experience").alias("count_exp")
            ).collect()[0]
            
            # Escribir estadísticas de experiencia
            exp_row = self.spark.createDataFrame([{
                "stat_type": "base_experience",
                "avg_value": float(exp_stats["avg_exp"]) if exp_stats["avg_exp"] else 0.0,
                "max_value": int(exp_stats["max_exp"]) if exp_stats["max_exp"] else 0,
                "min_value": int(exp_stats["min_exp"]) if exp_stats["min_exp"] else 0,
                "count_pokemon": int(exp_stats["count_exp"]),
                "updated_at": current_timestamp()
            }])
            
            exp_row.write \
                .format("org.apache.spark.sql.cassandra") \
                .option("keyspace", "pokemon_data") \
                .option("table", "pokemon_stats") \
                .mode("append") \
                .save()
            
            # Escribir datos por tipo
            for row in df.collect():
                if row["types"]:  # Verificar que types no sea None
                    for pokemon_type in row["types"]:
                        type_row = self.spark.createDataFrame([{
                            "type": pokemon_type,
                            "pokemon_id": row["id"],
                            "pokemon_name": row["name"],
                            "base_experience": row["base_experience"],
                            "timestamp": row["timestamp"]
                        }])
                        
                        type_row.write \
                            .format("org.apache.spark.sql.cassandra") \
                            .option("keyspace", "pokemon_data") \
                            .option("table", "pokemon_by_type") \
                            .mode("append") \
                            .save()
            
            logger.info(f"Batch {epoch_id}: Estadísticas actualizadas")
            df.unpersist()
            
        except Exception as e:
            logger.error(f"Error escribiendo estadísticas: {e}")
            if hasattr(df, 'unpersist'):
                df.unpersist()

    def run(self):
        """Ejecutar el procesador"""
        logger.info("Iniciando procesador Spark de Pokemon...")
        
        # Crear stream de Kafka
        kafka_df = self.create_kafka_stream()
        
        # Stream de debug
        debug_query = kafka_df.writeStream \
            .foreachBatch(self.debug_kafka_data) \
            .outputMode("append") \
            .trigger(processingTime='15 seconds') \
            .start()
        
        # Procesar datos
        processed_df = self.process_pokemon_data(kafka_df)
        
        # Query 1: Escribir datos raw
        query1 = processed_df.writeStream \
            .foreachBatch(self.write_to_cassandra_raw) \
            .outputMode("append") \
            .trigger(processingTime='20 seconds') \
            .start()
        
        # Query 2: Escribir estadísticas
        query2 = processed_df.writeStream \
            .foreachBatch(self.write_pokemon_stats) \
            .outputMode("append") \
            .trigger(processingTime='30 seconds') \
            .start()
        
        try:
            # Esperar todos los queries
            query1.awaitTermination()
        except KeyboardInterrupt:
            logger.info("Deteniendo procesador...")
            debug_query.stop()
            query1.stop()
            query2.stop()
            self.spark.stop()

if __name__ == "__main__":
    processor = PokemonSparkProcessor()
    processor.run()