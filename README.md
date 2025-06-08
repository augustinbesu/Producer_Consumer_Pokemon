# Pokemon Streaming Analytics

Un proyecto de ejemplo que demuestra la implementación de un pipeline completo de datos en tiempo real, utilizando Pokemon como dataset de ejemplo para ilustrar conceptos fundamentales de big data y sistemas distribuidos.

**Desarrollado por: Augustin Alexandru Besu**

## Arquitectura del Sistema

```
PokeAPI → Kafka Producer → Kafka Cluster → Spark Streaming → Cassandra
                                                ↓
                                         REST API ← Grafana Dashboard
                                                ↓
                                         Jupyter Analytics
```

### Componentes Principales

- **Producer**: Obtiene datos de Pokemon desde PokeAPI y los envía a Kafka
- **Kafka**: Sistema de streaming distribuido para manejo de datos en tiempo real
- **Spark**: Procesamiento de streams en tiempo real con escritura a Cassandra
- **Cassandra**: Base de datos NoSQL para almacenamiento escalable
- **API REST**: Exposición de datos para Grafana
- **Grafana**: Dashboard de visualización en tiempo real
- **Jupyter**: Análisis interactivo y exploración de datos

## Inicio Rápido

### Prerrequisitos
- Docker y Docker Compose
- Al menos 8GB RAM disponible
- Puertos libres: 8080, 8888, 3000, 9042, 29092, 5000

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <tu-repo>
   cd pokemon-streaming
   ```

2. **Configuración completa automática**:
   ```bash
   make setup
   ```
   
   Este comando:
   - Construye todas las imágenes Docker
   - Levanta todos los servicios
   - Configura Kafka con el topic necesario
   - Inicializa Cassandra con las tablas requeridas

3. **Verificar el estado**:
   ```bash
   make status
   make check-cassandra
   ```

## Servicios y Acceso

| Servicio | URL | Credenciales | Descripción |
|----------|-----|--------------|-------------|
| **Grafana Dashboard** | http://localhost:3000 | admin/pokemon123 | Visualización en tiempo real |
| **Jupyter Lab** | http://localhost:8888 | token: pokemon123 | Análisis interactivo |
| **REST API** | http://localhost:5000 | - | API de datos Pokemon |
| **Spark Master UI** | http://localhost:8080 | - | Monitoreo de Spark |
| **Kafka** | localhost:29092 | - | Broker de mensajes |
| **Cassandra** | localhost:9042 | - | Base de datos |

## Estructura de Datos

### Tabla `raw_pokemon`
```sql
CREATE TABLE raw_pokemon (
    id int PRIMARY KEY,
    name text,
    height int,
    weight int,
    base_experience int,
    types list<text>,
    abilities list<text>,
    stats map<text, int>,
    timestamp timestamp
);
```

### Tabla `pokemon_stats`
```sql
CREATE TABLE pokemon_stats (
    stat_type text PRIMARY KEY,
    avg_value double,
    max_value int,
    min_value int,
    count_pokemon bigint,
    updated_at timestamp
);
```

### Tabla `pokemon_by_type`
```sql
CREATE TABLE pokemon_by_type (
    type text,
    pokemon_id int,
    pokemon_name text,
    base_experience int,
    timestamp timestamp,
    PRIMARY KEY (type, pokemon_id)
);
```

## Funcionalidades Principales

### Dashboard de Grafana
- **Total Pokemon Procesados**: Contador en tiempo real
- **Pokemon por Tiempo**: Gráfico temporal de procesamiento
- **Distribución por Tipos**: Top 5 tipos más comunes
- **Top Pokemon por Experiencia**: Ranking de Pokemon más poderosos

### Jupyter Analytics
- Análisis exploratorio de datos
- Visualizaciones interactivas con Plotly
- Estadísticas por tipo de Pokemon
- Análisis de correlaciones entre atributos

### API REST Endpoints
```
GET  /health                    # Estado del servicio
GET  /api/total-pokemon        # Total de Pokemon procesados
GET  /api/type-distribution    # Distribución por tipos
GET  /api/top-pokemon          # Top Pokemon por experiencia
GET  /api/pokemon-by-hour      # Pokemon procesados por hora
POST /query                    # Endpoint principal para Grafana
POST /search                   # Búsqueda de métricas disponibles
```

## Comandos Útiles

### Monitoreo
```bash
# Ver estado de todos los servicios
make status

# Ver logs en tiempo real
make logs

# Ver logs específicos
make logs-producer    # Logs del productor
make logs-spark      # Logs de Spark
make logs-grafana    # Logs de Grafana
```

### Verificación de Datos
```bash
# Verificar datos en Cassandra
make check-cassandra

# Verificar topics de Kafka
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Ver datos raw en Cassandra
docker exec cassandra cqlsh -e "SELECT * FROM pokemon_data.raw_pokemon LIMIT 10;"
```

### Gestión de Servicios
```bash
# Reiniciar servicios específicos
make restart-producer
make restart-spark
make restart-grafana

# Limpiar todo el sistema
make clean

# Reconstruir desde cero
make setup
```

## Pipeline de Datos en Detalle

### 1. Ingesta de Datos
- **Frecuencia**: Cada 3-8 segundos (aleatorio)
- **Fuente**: PokeAPI (https://pokeapi.co/)
- **Formato**: JSON con atributos completos del Pokemon
- **Volumen**: ~100-200 Pokemon/hora

### 2. Streaming con Kafka
- **Topic**: `pokemon-data`
- **Particiones**: 3
- **Replicación**: 1 (desarrollo)
- **Retención**: 24 horas

### 3. Procesamiento con Spark
- **Trigger**: Cada 10-20 segundos
- **Operaciones**: 
  - Parseo de JSON
  - Limpieza de datos
  - Cálculo de estadísticas agregadas
  - Escritura a múltiples tablas

### 4. Almacenamiento en Cassandra
- **Estrategia**: SimpleStrategy
- **Factor de replicación**: 1
- **Consistency Level**: ONE (desarrollo)

## Troubleshooting

### Problemas Comunes

**Servicios no inician**:
```bash
# Verificar logs específicos
docker compose logs <nombre-servicio>

# Verificar recursos
docker system df
```

**Cassandra no responde**:
```bash
# Cassandra necesita tiempo para inicializar (1-2 minutos)
# Verificar estado
docker exec cassandra nodetool status
```

**Spark no conecta a Cassandra**:
```bash
# Verificar conectividad
docker exec spark-processor ping cassandra

# Reiniciar procesador
make restart-spark
```

**Grafana no muestra datos**:
```bash
# Verificar API
curl http://localhost:5000/api/total-pokemon

# Verificar datasource en Grafana
# Admin → Data Sources → Test connection
```

### Logs Importantes

**Productor funcionando**:
```
INFO - Obtenido Pokemon: charizard (id: 6)
INFO - Enviado a Kafka: pokemon-data
```

**Spark procesando**:
```
INFO - Batch 5: Escribiendo 3 registros a Cassandra...
INFO - Batch 5: 3 registros escritos a raw_pokemon
```

**API funcionando**:
```
INFO - Conectado a Cassandra
INFO - get_type_distribution devolvió 15 tipos
```

## Tecnologías Utilizadas

- **Docker**: Containerización y orquestación
- **Apache Kafka**: Streaming de datos en tiempo real
- **Apache Spark**: Procesamiento distribuido de streams
- **Apache Cassandra**: Base de datos NoSQL distribuida
- **Flask**: API REST ligera
- **Grafana**: Dashboards y visualización
- **Jupyter**: Análisis interactivo de datos
- **Python**: Lenguaje principal del proyecto

## Posibles Extensiones

- **Kafka Connect**: Para conectores automáticos
- **Apache Airflow**: Para orquestación de workflows
- **Redis**: Para caché de consultas frecuentes
- **Elasticsearch**: Para búsquedas textuales avanzadas
- **Machine Learning**: Para predicciones sobre Pokemon

## Métricas de Rendimiento

En un entorno típico de desarrollo:
- **Latencia de ingesta**: < 100ms
- **Throughput de Kafka**: 100-1000 mensajes/segundo
- **Latencia de Spark**: 10-30 segundos por batch
- **Consultas de API**: < 200ms promedio
- **Actualización de Grafana**: Cada 5 segundos

---

**Nota**: Este proyecto está diseñado para fines educativos y demostración de tecnologías de big data. Para producción, considerar configuraciones adicionales de seguridad, monitoreo y escalabilidad.