FROM openjdk:11-jre-slim

# Variables de entorno
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Spark
RUN wget -q "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && tar xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Instalar Python y dependencias con versiones compatibles
RUN pip3 install --no-cache-dir \
    pyspark==3.5.0 \
    cassandra-driver==3.29.1 \
    pandas==2.0.3 \
    numpy==1.24.3

# Descargar conectores compatibles con Spark 3.5.0
WORKDIR $SPARK_HOME/jars

# Kafka connector
RUN wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar

# Kafka clients
RUN wget -q https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar

# Spark token provider
RUN wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar

# Commons pool
RUN wget -q https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# CASSANDRA CONNECTOR COMPLETO - VERSIÓN CORRECTA (3.4.0)
RUN wget -q https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.12/3.4.0/spark-cassandra-connector_2.12-3.4.0.jar

# Assembly completo del conector que incluye todas las clases
RUN wget -q https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector-assembly_2.12/3.4.0/spark-cassandra-connector-assembly_2.12-3.4.0.jar

# TYPESAFE CONFIG - DEPENDENCIA CRÍTICA FALTANTE
RUN wget -q https://repo1.maven.org/maven2/com/typesafe/config/1.4.2/config-1.4.2.jar

# Driver de Cassandra Java - VERSIONES COMPATIBLES (4.14.1)
RUN wget -q https://repo1.maven.org/maven2/com/datastax/oss/java-driver-core/4.14.1/java-driver-core-4.14.1.jar && \
    wget -q https://repo1.maven.org/maven2/com/datastax/oss/java-driver-query-builder/4.14.1/java-driver-query-builder-4.14.1.jar && \
    wget -q https://repo1.maven.org/maven2/com/datastax/oss/java-driver-mapper-runtime/4.14.1/java-driver-mapper-runtime-4.14.1.jar && \
    wget -q https://repo1.maven.org/maven2/com/datastax/oss/java-driver-shaded-guava/25.1-jre/java-driver-shaded-guava-25.1-jre.jar

# Dependencias JNR - VERSIONES COMPATIBLES
RUN wget -q https://repo1.maven.org/maven2/com/github/jnr/jffi/1.3.9/jffi-1.3.9.jar && \
    wget -q https://repo1.maven.org/maven2/com/github/jnr/jnr-ffi/2.2.11/jnr-ffi-2.2.11.jar && \
    wget -q https://repo1.maven.org/maven2/com/github/jnr/jnr-posix/3.1.7/jnr-posix-3.1.7.jar && \
    wget -q https://repo1.maven.org/maven2/com/github/jnr/jnr-constants/0.10.4/jnr-constants-0.10.4.jar

# Netty dependencies - VERSIÓN COMPATIBLE
RUN wget -q https://repo1.maven.org/maven2/io/netty/netty-handler/4.1.86.Final/netty-handler-4.1.86.Final.jar && \
    wget -q https://repo1.maven.org/maven2/io/netty/netty-transport-native-epoll/4.1.86.Final/netty-transport-native-epoll-4.1.86.Final.jar && \
    wget -q https://repo1.maven.org/maven2/io/netty/netty-common/4.1.86.Final/netty-common-4.1.86.Final.jar && \
    wget -q https://repo1.maven.org/maven2/io/netty/netty-buffer/4.1.86.Final/netty-buffer-4.1.86.Final.jar && \
    wget -q https://repo1.maven.org/maven2/io/netty/netty-transport/4.1.86.Final/netty-transport-4.1.86.Final.jar && \
    wget -q https://repo1.maven.org/maven2/io/netty/netty-codec/4.1.86.Final/netty-codec-4.1.86.Final.jar

# Scala reflect
RUN wget -q https://repo1.maven.org/maven2/org/scala-lang/scala-reflect/2.12.17/scala-reflect-2.12.17.jar

WORKDIR /app
COPY pokemon_processor.py .
COPY requirements.txt .

# Crear usuario spark
RUN useradd -ms /bin/bash spark
USER spark

# Script de inicio
CMD ["python3", "pokemon_processor.py"]