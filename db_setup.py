import sqlite3
import random
import os

# Caminho para o banco de dados
DB_FILE = 'providers.db'

def populate_database(db_name=DB_FILE, num_providers=100): # Aumentei para 100 profissionais
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # (Opcional) Remover a tabela existente para recriar com novos dados
        cursor.execute("DROP TABLE IF EXISTS providers")

        # Cria a tabela de profissionais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS providers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                servico TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                contato TEXT,
                disponivel BOOLEAN NOT NULL DEFAULT 1,
                avaliacoes INTEGER NOT NULL DEFAULT 0
            )
        ''')

        services = [
            "Encanador", "Eletricista", "Faxineira", "Chaveiro", "Marceneiro",
            "Pedreiro", "Doméstica", "Jardineiro", "Pintor", "Técnico de Ar Condicionado",
            "Montador de Móveis", "Limpeza de Estofados", "Diarista", "Marmorista"
        ]

        # Localizações representativas em Brasília (DF)
        locations_brasilia_areas = [
            (-15.7942, -47.8822),   # Plano Piloto (Centro)
            (-15.8200, -47.9000),   # Sudoeste
            (-15.7550, -47.8650),   # Asa Norte
            (-15.8400, -47.9200),   # Guará
            (-15.8373, -47.9014),   # Lago Sul
            (-15.7801, -47.8340),   # Lago Norte
            (-16.0357, -48.0543),   # Ceilândia
            (-15.8429, -48.0654),   # Taguatinga
            (-15.9678, -48.0032),   # Águas Claras
            (-15.9761, -47.9228),   # Samambaia
            (-15.8821, -48.0772),   # Gama
            (-15.8797, -47.9657),   # Recanto das Emas
            (-15.8500, -47.7800),   # São Sebastião
            (-15.7700, -47.8000)    # Paranoá
        ]

        profissionais_data = []
        for i in range(num_providers):
            nome = f"Profissional {chr(65 + random.randint(0, 25))}{chr(65 + random.randint(0, 25))}" # Nomes tipo "Profissional AB"
            servico = random.choice(services)

            base_lat, base_lon = random.choice(locations_brasilia_areas)
            latitude = base_lat + random.uniform(-0.02, 0.02) # Variação de +/- 2km aprox.
            longitude = base_lon + random.uniform(-0.02, 0.02)

            contato = f"619{random.randint(80000000, 99999999)}" # Telefone (61) 9xxxx-xxxx
            disponivel = random.choice([0, 1]) # 0 para false, 1 para true
            avaliacoes = random.randint(5, 500) # Número de avaliações fictício

            profissionais_data.append((nome, servico, latitude, longitude, contato, disponivel, avaliacoes))

        cursor.executemany('''
            INSERT INTO providers (nome, servico, latitude, longitude, contato, disponivel, avaliacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', profissionais_data)

        conn.commit()
        print(f"Banco de dados '{db_name}' recriado e populado com {num_providers} profissionais.")

    except sqlite3.Error as e:
        print(f"Erro no SQLite: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    populate_database()