#from typing import Optional

class Product:
    def __init__(self, pk: int, name: str, price: float, restaurant_id: int):
        self.pk = pk  # PK gerado pelo banco
        self.name = name
        self.price = price
        self.restaurant_id = restaurant_id  # FK obrigatória

    def __str__(self):
        return f"{self.name}"

    def to_dict(self):
        return self._to_dict_privado()

    def _to_dict_privado(self) -> dict: # Retorna em forma de dicionario o produto
        return {
            "pk": self.pk,
            "name": self.name,
            "price": self.price,
            "restaurant_id": self.restaurant_id # FK apontando para a ID do Restaurante
        }