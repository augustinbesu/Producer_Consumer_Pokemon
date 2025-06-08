FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pokemon_producer.py .

CMD ["python", "pokemon_producer.py"]