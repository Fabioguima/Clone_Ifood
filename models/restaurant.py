from typing import List

from models.product import Product
from database.geradorpk.pk import Geradorpk



class Restaurant:
    def __init__(self,
                 pk: int,
                 email: str,
                 password: str,
                 restaurant_name: str,
                 commission: int,
                 menu: List[Product]
                 ):
        self.pk = Geradorpk.gerador_pk('Restaurant') # Gera automaticamente uma chave primária (PK) para o restaurante
        self.email = email
        self.password = password
        self.commission = commission
        self.restaurant_name = restaurant_name
        self.menu = menu

    def __str__(self):
        return f'{self.restaurant_name}'   

    def verifica_email(self):               
        self.email = self.email.lower()

        # Precisa ter um único @
        if "@" not in self.email or self.email.count("@") != 1:
            return False

        usuario, dominio_extensao = self.email.split("@")

        # O domínio precisa ter pelo menos um ponto e somente um
        if "." not in dominio_extensao or dominio_extensao.count(".") != 1:
            return False

        partes = dominio_extensao.split(".")
        dominio = partes[0]
        extensao = partes[-1]  # pega só a última parte

        # Nenhum campo pode estar vazio
        if not usuario or not dominio or not extensao:
            return False

        # Validação de caracteres
        if not usuario.isalnum() or not dominio.isalnum() or not extensao.isalpha():
            return False

        return True

    def verifica_senha(self): # Validação de senha
        if len(self.password) < 5:
            return 'Senha com menos de 5 caracteres'
        elif not any(c.isupper() for c in self.password): # Verifica se ao menos um elemento é verdadeiro
            return 'A senha não contém letra maiúscula'
        elif not any(d.islower() for d in self.password):
            return 'A senha não contém letra minúscula'
        elif not any(e.isdigit() for e in self.password):
            return 'A senha não contém número'
        else:
            return True

    @staticmethod
    def validate_commission(commission: int) -> bool: # Comissão deve ser um número inteiro maior ou igual a 0.
        if int(commission) >= 0:
            return True
        return False
    
    def verifica_nome(self: str) -> bool: # Verifica se o nome do restaurante possui mais de 10 caracteres.
            if len(self.restaurant_name) > 10:
                return True
            return False
        
    def to_dict(self) -> list[dict]:  # Retorna um dicionário com todos os dados do restaurante.
        return {
            'pk' : self.pk,
            'email' : self.email,
            'password' : self.password,
            'restaurant_name' : self.restaurant_name,
            'commission' : self.commission,
            'menu' : self.menu
        }
    
    def verificar_tudo(self): # Verificação completa e salvamento no banco
        from database.db import DB
        restaurantes = DB.load_json()  # Carrega lista de restaurantes

        # Verifica duplicidade
        for restaurante in restaurantes:
            if restaurante['restaurant_name'] == self.restaurant_name:
                return "O restaurante já existe."
            if restaurante['email'] == self.email:
                return "Email já cadastrado."
            
        # Verifica comissão
        if not Restaurant.validate_commission(self.commission):
            return "A comissão deve ser maior ou igual a 0."

        # Verifica email
        if not self.verifica_email():
            return "Email inválido."

        # Verifica senha
        senha_ok = self.verifica_senha()
        if senha_ok is not True:
            return senha_ok   # retorna mensagem de erro da função

        # Verifica nome
        if not self.verifica_nome():
            return "O nome do restaurante deve ter mais de 10 caracteres."

        # Se passou por todas as verificações -> salvar
        
        novo_restaurante = self.to_dict()
        restaurantes.append(novo_restaurante)
        DB.dump_json(restaurantes)   # salva usando o DB
        return f"Restaurante '{self.restaurant_name}' cadastrado com sucesso!"