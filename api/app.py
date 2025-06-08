from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class CassandraAPI:
    def __init__(self):
        self.cluster = None
        self.session = None
        self.connect()
    
    def connect(self):
        try:
            self.cluster = Cluster(['cassandra'])
            self.session = self.cluster.connect('pokemon_data')
            logging.info("Conectado a Cassandra")
        except Exception as e:
            logging.error(f"Error conectando a Cassandra: {e}")
    
    def get_total_pokemon(self):
        """Total de Pokemon procesados"""
        try:
            if not self.session:
                return 0
            result = self.session.execute("SELECT COUNT(*) as total FROM raw_pokemon")
            total = result.one().total
            return total
        except Exception as e:
            logging.error(f"Error get_total_pokemon: {e}")
            return 0
    
    def get_type_distribution(self):
        """Distribución por tipos"""
        try:
            if not self.session:
                return []

            query = "SELECT types FROM raw_pokemon"
            result = self.session.execute(query)
            
            type_counts = defaultdict(int)
            
            for row in result:
                if row.types and hasattr(row.types, '__iter__') and not isinstance(row.types, str):
                    for pokemon_type in row.types:
                        if pokemon_type:
                            type_counts[pokemon_type] += 1

            distribution = [
                {"type": type_name, "count": count} 
                for type_name, count in type_counts.items()
            ]
            
            # Devolver top 5 para simplicidad
            return sorted(distribution, key=lambda x: x['count'], reverse=True)[:5]

        except Exception as e:
            logging.error(f"Error en get_type_distribution: {e}")
            return []
    
    def get_top_pokemon(self, limit=5):
        """Top Pokemon por experiencia"""
        try:
            if not self.session:
                return []
            result = self.session.execute("SELECT name, base_experience FROM raw_pokemon")
            data = []
            for row in result:
                if row.base_experience and row.base_experience > 0:
                    data.append({
                        "name": row.name,
                        "base_experience": row.base_experience
                    })
            return sorted(data, key=lambda x: x['base_experience'], reverse=True)[:limit]
        except Exception as e:
            logging.error(f"Error get_top_pokemon: {e}")
            return []
    
    def get_pokemon_by_time(self):
        """Pokemon procesados por tiempo - Simulado"""
        try:
            total = self.get_total_pokemon()
            now = datetime.now()
            data = []
            intervals = 6
            per_interval = max(1, total // intervals)
            
            for i in range(intervals):
                time_point = now - timedelta(hours=i)
                timestamp = int(time_point.timestamp() * 1000)
                data.append([per_interval, timestamp])
            
            return sorted(data, key=lambda x: x[1])
            
        except Exception as e:
            logging.error(f"Error get_pokemon_by_time: {e}")
            return []

cassandra_api = CassandraAPI()

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "pokemon-api"})

@app.route('/')
def index():
    return jsonify({"message": "Pokemon API is running", "endpoints": ["/health", "/query", "/search"]})

@app.route('/search', methods=['POST'])
def search():
    """Endpoint para búsqueda de métricas"""
    return jsonify([
        "total-pokemon",
        "pokemon-by-hour", 
        "type-distribution",
        "top-pokemon"
    ])

@app.route('/query', methods=['POST'])
def query():
    """Endpoint principal para queries de Grafana"""
    try:
        data = request.get_json()
        results = []
        
        for target in data.get('targets', []):
            metric = target.get('target')
            
            if metric == 'total-pokemon':
                total = cassandra_api.get_total_pokemon()
                results.append({
                    "target": "Total Pokemon",
                    "datapoints": [[total, int(datetime.now().timestamp() * 1000)]]
                })
                
            elif metric == 'type-distribution':
                type_data = cassandra_api.get_type_distribution()
                for item in type_data:
                    results.append({
                        "target": f"{item['type'].title()}",
                        "datapoints": [[item['count'], int(datetime.now().timestamp() * 1000)]]
                    })
                    
            elif metric == 'top-pokemon':
                pokemon_data = cassandra_api.get_top_pokemon()
                for item in pokemon_data:
                    results.append({
                        "target": item['name'].title(),
                        "datapoints": [[item['base_experience'], int(datetime.now().timestamp() * 1000)]]
                    })
                    
            elif metric == 'pokemon-by-hour':
                time_data = cassandra_api.get_pokemon_by_time()
                results.append({
                    "target": "Pokemon per Hour",
                    "datapoints": time_data
                })
        
        return jsonify(results)
    
    except Exception as e:
        logging.error(f"Error in query endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)