from database.geradorpk.pk import Geradorpk

class Product:
    def __init__(self, pk: int, name: str, price: float):
        # 'id' é uma função built-in do Python: prefira usar 'pk' (Primary Key).
        self.pk = Geradorpk.gerador_pk('Product') # Gera um PK automaticamente
        self.name = name
        self.price = price

    def __str__(self):
        return f'{self.name}'

    def to_dict(self): # Converte o objeto Product em um dicionário (usado para salvar em JSON)
        return {
            'pk': self.pk,
            'name': self.name,
            'price': self.price
        }
    
