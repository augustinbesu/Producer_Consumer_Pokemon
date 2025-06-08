FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pokemon_consumer.py .

CMD ["python", "pokemon_consumer.py"]