FROM jupyter/pyspark-notebook:latest

USER root

# Instalar dependencias adicionales
RUN pip install --no-cache-dir \
    kafka-python==2.0.2 \
    cassandra-driver==3.29.1 \
    requests==2.31.0 \
    plotly==5.17.0 \
    seaborn==0.12.2

USER $NB_UID

WORKDIR /home/jovyan/work