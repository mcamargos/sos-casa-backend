import os
import sqlite3
import math
from flask import Flask, jsonify, request
from flask_cors import CORS # Importa Flask-CORS
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas, permitindo que seu app mobile acesse a API

# Define o caminho para o banco de dados SQLite
# DATABASE_URL no .env deve ser 'sqlite:///providers.db'
DATABASE = os.getenv('DATABASE_URL').replace('sqlite:///', '')

# Função auxiliar para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Retorna linhas como objetos que podem ser acessados por nome da coluna
    return conn

# Função para calcular a distância entre duas coordenadas (Fórmula de Haversine simplificada)
# Apenas para fins de MVP. Para produção, considere bibliotecas mais robustas ou APIs de mapas.
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371 # Raio da Terra em quilômetros

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo ao Backend SOS Casa! Acesse /api/providers/search para buscar profissionais."})

@app.route('/api/providers/search', methods=['GET'])
def search_providers():
    service_type = request.args.get('service') # Tipo de serviço (ex: 'Encanador')
    user_lat = request.args.get('lat', type=float) # Latitude do usuário
    user_lon = request.args.get('lon', type=float) # Longitude do usuário

    if not service_type or user_lat is None or user_lon is None:
        return jsonify({"error": "Parâmetros 'service', 'lat' e 'lon' são obrigatórios."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca profissionais pelo tipo de serviço e que estão disponíveis
    query = "SELECT * FROM profissionais WHERE servico = ? AND disponivel = 1"
    cursor.execute(query, (service_type,))

    providers = []
    for row in cursor.fetchall():
        provider = dict(row) # Converte a linha SQLite em um dicionário

        # Calcula a distância entre o usuário e o profissional
        distance = haversine_distance(user_lat, user_lon, provider['latitude'], provider['longitude'])
        provider['distancia_km'] = round(distance, 2) # Adiciona a distância ao dicionário
        providers.append(provider)

    conn.close()

    # Opcional: Ordenar por distância
    providers.sort(key=lambda p: p['distancia_km'])

    return jsonify(providers)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)