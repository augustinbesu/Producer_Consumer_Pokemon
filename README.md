<div align="center">

# 🌟 Pokemon Streaming Analytics

**Ejemplo práctico de arquitectura Producer-Consumer con tecnologías Big Data**

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)](https://kafka.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=for-the-badge&logo=apachespark&logoColor=black)](https://spark.apache.org/)
[![Cassandra](https://img.shields.io/badge/cassandra-%231287B1.svg?style=for-the-badge&logo=apache-cassandra&logoColor=white)](https://cassandra.apache.org/)
[![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/)

*Un pipeline completo de datos en tiempo real utilizando Pokemon como dataset para demostrar conceptos fundamentales de sistemas distribuidos*

**Desarrollado por:** [Augustin Alexandru Besu](https://github.com/augustinbesu)

</div>

---

## 🎯 Objetivo del Proyecto

Este proyecto implementa una **arquitectura de streaming distribuida** completa, demostrando:

- ✅ **Patrón Producer-Consumer** con Apache Kafka
- ✅ **Stream Processing** en tiempo real con Apache Spark
- ✅ **Almacenamiento NoSQL** escalable con Cassandra
- ✅ **Visualización en tiempo real** con Grafana
- ✅ **Análisis interactivo** con Jupyter
- ✅ **APIs RESTful** para exposición de datos
- ✅ **Containerización completa** con Docker

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph TB
    %% Definición de estilos para los subgrafos
    classDef datasource fill:#e1f5fe,stroke:#039be5,stroke-width:2px
    classDef ingestion fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
    classDef broker fill:#fff3e0,stroke:#fb8c00,stroke-width:2px
    classDef processing fill:#e8f5e8,stroke:#43a047,stroke-width:2px
    classDef storage fill:#fce4ec,stroke:#e91e63,stroke-width:2px
    classDef api fill:#f1f8e9,stroke:#689f38,stroke-width:2px
    classDef visualization fill:#fff8e1,stroke:#ffa000,stroke-width:2px
    classDef analytics fill:#e3f2fd,stroke:#1976d2,stroke-width:2px

    %% Nodos principales (fuera de los subgrafos)
    A[🔗 PokeAPI]
    B[📡 Pokemon Producer<br/>Python]
    C[🚀 Apache Kafka<br/>Topic: pokemon-data]
    D[⚡ Apache Spark<br/>Streaming]
    E[🗄️ Apache Cassandra]
    F[🌐 REST API<br/>Flask]
    G[📊 Grafana Dashboard]
    H[📈 Jupyter Analytics]

    %% Subgrafos (solo para agrupación visual)
    subgraph "Data Source"
        A
    end
    
    subgraph "Data Ingestion"
        B
    end
    
    subgraph "Message Broker"
        C
    end
    
    subgraph "Stream Processing"
        D
    end
    
    subgraph "Storage Layer"
        E
    end
    
    subgraph "API Layer"
        F
    end
    
    subgraph "Visualization"
        G
    end
    
    subgraph "Analytics"
        H
    end

    %% Conexiones
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H

    %% Aplicar estilos
    class A datasource
    class B ingestion
    class C broker
    class D processing
    class E storage
    class F api
    class G visualization
    class H analytics
```

### 🔧 Componentes del Sistema

| Componente | Tecnología | Función | Puerto |
|------------|------------|---------|--------|
| **Data Producer** | Python + Requests | Obtiene datos de PokeAPI y envía a Kafka | - |
| **Message Broker** | Apache Kafka | Cola de mensajes distribuida | 29092 |
| **Stream Processor** | Apache Spark | Procesamiento en tiempo real | 8080 |
| **Database** | Apache Cassandra | Almacenamiento NoSQL escalable | 9042 |
| **REST API** | Flask | Exposición de datos | 5000 |
| **Dashboard** | Grafana | Visualización en tiempo real | 3000 |
| **Analytics** | Jupyter Lab | Análisis interactivo | 8888 |

---

## 🚀 Inicio Rápido

### 📋 Prerrequisitos

- 🐳 **Docker & Docker Compose** (v20.10+)
- 💾 **8GB RAM mínimo** disponible
- 🔌 **Puertos libres**: 3000, 5000, 8080, 8888, 9042, 29092

### ⚡ Instalación en 3 pasos

<details>
<summary>📁 <strong>1. Clonar el repositorio</strong></summary>

```bash
git clone https://github.com/augustinbesu/Producer_Consumer_Pokemon.git
cd Producer_Consumer_Pokemon
```
</details>

<details>
<summary>🔧 <strong>2. Desplegar el ecosistema completo</strong></summary>

```bash
make setup
```

**Este comando automáticamente:**
- 🏗️ Construye todas las imágenes Docker
- 🚀 Levanta todos los servicios
- ⚙️ Configura Kafka con topics
- 🗃️ Inicializa Cassandra con esquemas
- 🔄 Inicia el pipeline de datos

</details>

<details>
<summary>✅ <strong>3. Verificar el estado</strong></summary>

```bash
make status              # Estado general
make check-cassandra     # Verificar base de datos
make logs               # Ver logs en tiempo real
```
</details>

---

## 🌐 Interfaces de Usuario

<div align="center">

| 🖥️ Servicio | 🔗 URL | 🔐 Credenciales | 📝 Descripción |
|-------------|---------|-----------------|-----------------|
| **🎨 Grafana** | [localhost:3000](http://localhost:3000) | `admin` / `pokemon123` | Dashboard en tiempo real |
| **📊 Jupyter** | [localhost:8888](http://localhost:8888) | Token: `pokemon123` | Análisis de datos |
| **🔌 REST API** | [localhost:5000](http://localhost:5000) | - | API de datos |
| **⚡ Spark UI** | [localhost:8080](http://localhost:8080) | - | Monitor de Spark |

</div>

---

## 📊 Schema de Base de Datos

<details>
<summary>🗃️ <strong>Estructura de Cassandra</strong></summary>

### 📋 Tabla `raw_pokemon`
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

### 📈 Tabla `pokemon_stats`
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

### 🏷️ Tabla `pokemon_by_type`
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

</details>

---

## 🎯 Funcionalidades Principales

### 📊 Dashboard de Grafana
- 🔢 **Contador total** de Pokemon procesados
- ⏰ **Timeline** de procesamiento por hora
- 🥧 **Distribución circular** de tipos de Pokemon
- 🏆 **Ranking** de Pokemon por experiencia

### 🔬 Jupyter Analytics
- 📈 **Visualizaciones interactivas** con Plotly
- 📊 **Análisis estadístico** por tipos
- 🔍 **Exploración de datos** en tiempo real
- 📋 **Correlaciones** entre atributos

### 🔌 API REST Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Estado del servicio |
| `GET` | `/api/total-pokemon` | Total procesados |
| `GET` | `/api/type-distribution` | Distribución por tipos |
| `GET` | `/api/top-pokemon` | Top por experiencia |
| `POST` | `/query` | Endpoint para Grafana |

---

## 🛠️ Comandos de Gestión

<details>
<summary>👁️ <strong>Monitoreo</strong></summary>

```bash
make status              # Estado de servicios
make logs               # Logs en tiempo real
make logs-producer      # Logs del productor
make logs-spark         # Logs de Spark
make logs-grafana       # Logs de Grafana
```
</details>

<details>
<summary>🔍 <strong>Verificación</strong></summary>

```bash
make check-cassandra    # Datos en Cassandra
make check-kafka       # Topics de Kafka

# Consultas directas
docker exec cassandra cqlsh -e "SELECT COUNT(*) FROM pokemon_data.raw_pokemon;"
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic pokemon-data --from-beginning
```
</details>

<details>
<summary>🔄 <strong>Gestión de Servicios</strong></summary>

```bash
make restart-producer   # Reiniciar productor
make restart-spark      # Reiniciar Spark
make restart-grafana    # Reiniciar Grafana
make clean             # Limpiar todo
make setup             # Reconstruir completo
```
</details>

---

## 📈 Pipeline de Datos

### 1️⃣ **Ingesta** 
- **Fuente**: [PokeAPI](https://pokeapi.co/)
- **Frecuencia**: 3-8 segundos (aleatorio)
- **Formato**: JSON estructurado
- **Volumen**: ~100-200 Pokemon/hora

### 2️⃣ **Streaming**
- **Broker**: Apache Kafka
- **Topic**: `pokemon-data`
- **Particiones**: 3
- **Retención**: 24 horas

### 3️⃣ **Procesamiento**
- **Engine**: Apache Spark Streaming
- **Trigger**: Cada 10-20 segundos
- **Operaciones**: Parseo, limpieza, agregaciones

### 4️⃣ **Almacenamiento**
- **BD**: Apache Cassandra
- **Estrategia**: SimpleStrategy
- **Replicación**: Factor 1

---

## 🧰 Stack Tecnológico

<div align="center">

| Categoría | Tecnología | Versión | Propósito |
|-----------|------------|---------|-----------|
| **🐳 Contenedores** | Docker Compose | 3.8 | Orquestación |
| **📨 Streaming** | Apache Kafka | 2.8 | Message Broker |
| **⚡ Procesamiento** | Apache Spark | 3.3 | Stream Processing |
| **🗄️ Base de Datos** | Apache Cassandra | 4.0 | NoSQL Storage |
| **🌐 API** | Flask | 2.3 | REST Services |
| **📊 Visualización** | Grafana | 9.0 | Dashboards |
| **🔬 Analytics** | Jupyter Lab | 3.6 | Data Science |
| **🐍 Lenguaje** | Python | 3.9 | Backend |

</div>

---

## 🚨 Troubleshooting

<details>
<summary>⚠️ <strong>Problemas Comunes</strong></summary>

### 🔴 Servicios no inician
```bash
docker compose logs <servicio>
docker system df  # Verificar espacio en disco
make clean        # Limpiar recursos
```

### 🟡 Cassandra no responde
```bash
# Esperar 1-2 minutos para inicialización completa
docker exec cassandra nodetool status
docker exec cassandra cqlsh -e "DESCRIBE KEYSPACES;"
```

### 🟠 Spark desconectado de Cassandra
```bash
docker exec spark-processor ping cassandra
make restart-spark
docker compose logs spark-processor
```

### 🔵 **Grafana no muestra datos (API 404)**
**Síntoma:** Los endpoints `/api/total-pokemon` devuelven 404
**Causa:** Docker está ejecutando versión anterior del código sin los nuevos endpoints

**Solución:**
```bash
# Reconstruir específicamente la API
docker compose stop pokemon-api
docker compose build --no-cache pokemon-api
docker compose up -d pokemon-api

# Verificar que funciona
curl http://localhost:5000/api/total-pokemon
# Debería devolver: {"total": X}
```

### 🟣 Kafka topic no existe
```bash
# Crear topic manualmente si falla kafka-setup.sh
docker exec kafka kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 3 \
    --topic pokemon-data
```

### 🟢 **Script bash no ejecuta (WSL/Linux)**
**Síntoma:** `./kafka-setup.sh: cannot execute: required file not found`
**Causa:** Archivos creados en Windows con line endings CRLF

**Solución:**
```bash
# Opción 1: Usar dos2unix
dos2unix kafka-setup.sh
chmod +x kafka-setup.sh

# Opción 2: Recrear archivo
rm kafka-setup.sh
cat > kafka-setup.sh << 'EOF'
#!/bin/bash
echo "Creando topic pokemon-data..."
docker exec kafka kafka-topics --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 3 \
    --topic pokemon-data
EOF
chmod +x kafka-setup.sh
```

### ⚫ Producer no conecta a PokeAPI
```bash
# Verificar conectividad
docker exec pokemon-producer ping 8.8.8.8
docker exec pokemon-producer curl https://pokeapi.co/api/v2/pokemon/1
```

</details>

<details>
<summary>📋 <strong>Logs de Verificación</strong></summary>

**✅ Productor funcionando:**
```
INFO - Pokemon magnemite enviado - Partition: 0, Offset: 5
INFO - Pokemon dragonite enviado - Partition: 0, Offset: 6
```

**✅ Spark procesando:**
```
INFO - Batch 5: Escribiendo 3 registros a Cassandra
INFO - Batch 5: 3 registros escritos a raw_pokemon
```

**✅ API funcionando:**
```
INFO - Conectado a Cassandra
INFO:werkzeug:172.18.0.1 - - [GET /api/total-pokemon HTTP/1.1] 200 -
```

**✅ Cassandra con datos:**
```bash
$ make check-cassandra
 count
-------
    25
```

**❌ API con imagen antigua:**
```
INFO:werkzeug:172.18.0.1 - - [GET /api/total-pokemon HTTP/1.1] 404 -
```

</details>

<details>
<summary>🔧 <strong>Comandos de Diagnóstico Rápido</strong></summary>

```bash
# Pipeline completo
make status                           # Estado general
curl http://localhost:5000/health     # API health check
curl http://localhost:5000/api/total-pokemon  # Endpoint específico
make check-cassandra                  # Datos en BD

# Verificar flujo de datos
make logs-producer | grep "enviado"   # Pokemon siendo enviados
make logs-spark | grep "registros"    # Batches procesados
docker exec kafka kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic pokemon-data --max-messages 3  # Mensajes en Kafka
```

</details>

<details>
<summary>🚀 <strong>Reinicio Limpio</strong></summary>

**Si nada funciona, reinicio completo:**
```bash
# Parar todo
docker compose down

# Limpiar imágenes y volúmenes
docker compose down -v
docker system prune -f

# Reconstruir desde cero
make setup

# Esperar 2-3 minutos y verificar
make status
curl http://localhost:5000/api/total-pokemon
```

</details>

---

## 📊 Métricas de Rendimiento

<div align="center">

| Métrica | Valor Típico | Descripción |
|---------|--------------|-------------|
| **⚡ Latencia de ingesta** | < 100ms | Tiempo desde API hasta Kafka |
| **🚀 Throughput Kafka** | 100-1K msg/seg | Capacidad de mensajes |
| **⏱️ Latencia Spark** | 10-30 segundos | Procesamiento por batch |
| **🔌 API Response** | < 200ms | Tiempo de respuesta |
| **📊 Actualización Grafana** | 5 segundos | Frecuencia de refresh |

</div>

---

## 🔮 Posibles Extensiones

- 🔗 **Kafka Connect** para conectores automáticos
- 🌊 **Apache Airflow** para orquestación de workflows  
- ⚡ **Redis** para caché de consultas frecuentes
- 🔍 **Elasticsearch** para búsquedas textuales
- 🤖 **Machine Learning** para predicciones de Pokemon
- 🔒 **Security** con autenticación y autorización
- 🌍 **Kubernetes** para despliegue en producción

---

<div align="center">

## 🎓 Fines Educativos

> Este proyecto está diseñado para **demostrar conceptos de Big Data** y **sistemas distribuidos**. 
> Para entornos de producción, considerar configuraciones adicionales de **seguridad**, **monitoreo** y **escalabilidad**.

</div>
