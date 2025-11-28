import sqlite3
import os
from models.restaurant import Restaurant


class DB:
    # Caminho ABSOLUTO e FIXO do banco
    DB_PATH = os.path.join(os.path.dirname(__file__), "restaurants.db")

    # Garante que as tabelas são criadas apenas 1 vez
    tables_created = False

    def __init__(self):
        self.__setup_tables()

    # Função auxiliar para abrir conexão nova --> SEMPRE <--
    def __connect(self):
        conn = sqlite3.connect(DB.DB_PATH) # Abre o banco
        conn.row_factory = sqlite3.Row # Linhas retornam como dicionário
        conn.execute("PRAGMA foreign_keys = ON;") # Ativa foreign keys
        return conn # Retorna a conexão pronta
    
    def get_conn(self):
        return self.__connect()


    def __setup_tables(self): # Criação de Tabelas
        if DB.tables_created:  # já criou → não cria de novo
            return


        conn = self.get_conn()
        cur = conn.cursor()

        # Cria a tabela de Restaurant caso não exista
        cur.execute('''
            CREATE TABLE IF NOT EXISTS restaurant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_name TEXT NOT NULL,
                commission FLOAT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        ''')

        # Cria a tabela de Product caso não exista
        cur.execute('''
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco FLOAT NOT NULL,
                restaurant_id INTEGER NOT NULL,
                FOREIGN KEY (restaurant_id) REFERENCES restaurant(id)
            );
        ''')

        conn.commit() # Salva o BD
        conn.close() # Fecha o DB

        DB.tables_created = True  # marca como criado


    #----------------------------------------
    # CRUD dos Restaurantes
    #----------------------------------------

    def create_restaurant(self, restaurant: Restaurant): # Cria o Restaurante
        conn = self.get_conn()
        cur = conn.cursor()

        name_lc = restaurant.restaurant_name.strip().lower() # Garante nome lowercase

        cur.execute(
            '''
            INSERT INTO restaurant (restaurant_name, commission, email, password)
            VALUES (?, ?, ?, ?)
            ''',
            (
                name_lc,
                restaurant.commission,
                restaurant.email.lower().strip(),
                restaurant.password
            )
        )

        conn.commit()
        restaurant.pk = cur.lastrowid # ID que o banco acabou de criar, salva para ser usado posteriormente
        conn.close()

        return restaurant


    def login(self, email: str, password: str) -> Restaurant | None: # Login no restaurante
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute(
            '''
            SELECT * FROM restaurant
            WHERE email = ? AND password = ?
            ''',
            (email.lower().strip(), password)
        )

        row = cur.fetchone() # Retorna a primeira linha com email e password correspondente
        conn.close() # Fecha a conexão

        if not row: # Caso não existir a linha com email e password correspondente ele retorna None
            return None

        return Restaurant(
            pk=row["id"],
            restaurant_name=row["restaurant_name"],
            commission=row["commission"],
            email=row["email"],
            password=row["password"],
            menu=[]
        )


    def get_restaurants(self) -> list[dict]:
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute(
            '''
            SELECT r.id, r.restaurant_name, r.commission, p.nome, p.preco
            FROM restaurant r
            LEFT JOIN product p ON r.id = p.restaurant_id
            ORDER BY r.commission DESC, r.restaurant_name ASC
            '''
        )

        rows = cur.fetchall()
        conn.close()

        restaurantes = {}

        for row in rows:
            rid = row["id"]

            if rid not in restaurantes:
                restaurantes[rid] = {
                    "id": rid,
                    "restaurant_name": row["restaurant_name"],
                    "commission": row["commission"],
                    "products": []
                }

            # Percorre todas as linhas para adicionar os produtos
            if row["nome"] is not None:
                restaurantes[rid]["products"].append(
                    {"nome": row["nome"], "preco": row["preco"]}
                )

        return list(restaurantes.values()) # Retorna o restaurante completo com todos os produtos


    def exists_restaurant(self, email: str, restaurant_name: str) -> bool:  # Verifica a existência do restaurante
        conn = self.get_conn() # Conexão com o DB
        cur = conn.cursor() # Envia os comandos ao SQL

        cur.execute(
            '''
            SELECT id FROM restaurant
            WHERE email = ? OR LOWER(restaurant_name) = LOWER(?)
            ''',
            (email.lower().strip(), restaurant_name.lower().strip())
        )

        exists = cur.fetchone() is not None # Verifica se uma linha atende aos requisitos
        conn.close() # Fecha o DB

        return exists