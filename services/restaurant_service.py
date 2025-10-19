from database.db import DB
from models.product import Product
from models.restaurant import Restaurant

class RestaurantService:
    def __init__(self, email: str, password: str):
        self.db = DB() # Cria uma instância do banco de dados
        self.email = email
        self.password = password
        self.restaurant = self.db.get_restaurant(email, password) # Tenta autenticar o restaurante com base no e-mail e senha

    def is_authenticated(self) -> bool: #Retorna True se o restaurante estiver autenticado corretamente.
        return self.restaurant is not None
    
    def add_product(self, name: str, price: float) -> str: # Adiciona um novo produto ao menu do restaurante
        if not self.is_authenticated():
            return "Falha no login: restaurante não encontrado."
        
        # Validação do nome
        if len(name) <= 4:
            return "O nome do produto deve ter mais de 4 caracteres."
        
        # Validação do preço
        if price <= 0:
            return "O preço do produto deve ser maior que zero."
        
        restaurantes = self.db.load_json()

        # Encontra o restaurante autenticado
        for pk in restaurantes:
            if pk['pk'] == self.restaurant['pk']:
                for produto in pk['menu']:
                    if produto['name'].lower() == name.lower():
                        return f"O produto '{name}' já existe no menu de {self.restaurant['restaurant_name']}."

                # Cria um novo produto e adiciona ao menu
                product = Product(None, name, price)
                pk["menu"].append(product.to_dict())

                self.db.dump_json(restaurantes)

                return f"Produto '{name}' adicionado ao menu de {pk['restaurant_name']}."
        return "Restaurante não encontrado."

    def update_commission(self, commission: float) -> str: # Atualiza a comissão do restaurante autenticado.
        if not self.is_authenticated():
            return "Falha no login: restaurante não encontrado."
        
        if not Restaurant.validate_commission(commission):
            return "A comissão deve ser maior ou igual a 0."

        restaurantes = self.db.load_json()


        # Atualiza a comissão no restaurante correspondente
        for pk in restaurantes:
            if pk['pk'] == self.restaurant['pk']:
                pk["commission"] = int(commission)

                self.db.dump_json(restaurantes)

                return f"A comissão do {pk['restaurant_name']} foi atualizada para {commission}."
        return "Restaurante não encontrado."

    def delete_product(self, product_pk: int) -> str: # Exclui um produto do menu
        if not self.is_authenticated():
            return "Falha no login: restaurante não encontrado."
        
        restaurantes = self.db.load_json()

        # Busca o restaurante autenticado
        for pk in restaurantes:
            if pk['pk'] == self.restaurant['pk']:
                for menu in pk['menu']:
                    if menu['pk'] == product_pk:
                        nome_produto = menu['name']
                        pk['menu'].remove(menu)

                        self.db.dump_json(restaurantes)

                        return f"O produto {nome_produto} foi removido do menu --> {pk['restaurant_name']}."
        return "Produto não encontrado no menu."