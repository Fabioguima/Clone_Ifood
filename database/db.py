import json
from pathlib import Path
from models.restaurant import Restaurant


class DB:
    DATABASE = {}
    FILE_PATH = Path("database/restaurants/restaurantes.json")

    def __init__(self, add_fake_data=False):
        self.__setup_tables()

    def __setup_tables(self):
        self.DATABASE['RESTAURANTS'] = []

    # ---------------
    # Métodos  JSON
    # ---------------

    @classmethod
    def load_json(cls) -> list[dict]: # Lê os dados do arquivo JSON e retorna uma lista de dicionários. Caso o arquivo ainda não exista ou esteja vazio, retorna uma lista vazia.
        """Carrega dados do arquivo JSON"""
        if not cls.FILE_PATH.exists():
            return []
        with open(cls.FILE_PATH, "r", encoding="utf-8") as arquivo:
            try:
                return json.load(arquivo)
            except:
                return [] # Se o arquivo estiver corrompido ou com erro de leitura

    @classmethod
    def dump_json(cls, arquivo: list[dict]):
        """Grava dados no arquivo JSON"""
        cls.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)  # cria pasta se não existir
        with open(cls.FILE_PATH, "w", encoding="utf-8") as arq:
            json.dump(arquivo, arq, indent=4, ensure_ascii=False)

    def create_restaurant(self, restaurante: Restaurant): # Adiciona um novo restaurante ao banco de dados (arquivo JSON).
        restaurantes = self.load_json()
        restaurantes.append(restaurante.to_dict())  # garante que é dict
        self.dump_json(restaurantes)

    def login(self, email: str, password: str): # Faz o login de um restaurante verificando e-mail e senha.
        restaurantes = self.load_json()
        for dados in restaurantes:
            if dados['email'] == email and dados['password'] == password:
                return dados
        return None

    def get_restaurants(self): # Retorna a lista de restaurantes ordenada por Comissão (decrescente) e Nome (crescente)
        restaurantes = self.load_json()

        def criterio_de_ordenacao(restaurante: list[dict]):
            comissao = restaurante["commission"]
            nome = restaurante["restaurant_name"]
            return (-comissao, nome)

        return sorted(restaurantes, key=criterio_de_ordenacao) # Sorted() para ordenar a lista de restaurantes de acordo com o criterio

    def get_restaurant(self, email: str, password: str) -> Restaurant | None: # Retorna um restaurante específico autenticado com e-mail e senha.
        return self.login(email, password)