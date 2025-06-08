FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app.py .

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "app.py"]