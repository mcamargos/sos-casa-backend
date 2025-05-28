import sqlite3
import os

# Caminho para o banco de dados
DB_FILE = 'providers.db'
DB_PATH = os.path.join(os.path.dirname(__file__), DB_FILE)

def create_db_and_insert_data():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Cria a tabela de profissionais se ela não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profissionais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                servico TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                contato TEXT,
                disponivel BOOLEAN NOT NULL DEFAULT 1
            )
        ''')

        # Dados fictícios (latitude e longitude de áreas em Brasília - DF, Brasil)
        # Você pode ajustar esses valores para a sua região ou onde quiser simular
        profissionais_data = [
            ("Pedro Mendes", "Encanador", -15.8080, -47.8759, "(61) 9876-5432", True), # Eixo Monumental
            ("Ana Paula", "Faxineira", -15.8200, -47.9000, "(61) 9987-6543", True),    # Sudoeste
            ("Carlos Souza", "Eletricista", -15.7900, -47.8850, "(61) 9765-4321", False), # Asa Norte
            ("Maria Clara", "Faxineira", -15.8150, -47.8900, "(61) 9876-1234", True),    # Asa Sul
            ("José Alves", "Chaveiro", -15.8000, -47.8500, "(61) 9912-3456", True),    # Lago Norte
            ("Luiza Santos", "Encanador", -15.8400, -47.9200, "(61) 9876-0000", True),  # Guará
            ("Fernanda Lima", "Doméstica", -15.7700, -47.8000, "(61) 9912-1111", True), # Paranoá
            ("Rafaela Costa", "Faxineira", -15.8050, -47.8650, "(61) 9876-2222", True), # Plano Piloto
            ("Marcos Dantas", "Pedreiro", -15.8300, -47.9100, "(61) 9988-3333", True),  # Taguatinga
            ("Sofia Oliveira", "Eletricista", -15.8090, -47.8700, "(61) 9777-4444", True) # Noroeste
        ]

        # Insere os dados na tabela
        cursor.executemany("INSERT INTO profissionais (nome, servico, latitude, longitude, contato, disponivel) VALUES (?, ?, ?, ?, ?, ?)", profissionais_data)

        conn.commit()
        print(f"Banco de dados '{DB_FILE}' criado e dados inseridos com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro no SQLite: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_db_and_insert_data()