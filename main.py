from fastapi import FastAPI
from database.db import DB
from models.restaurant import Restaurant
from services.restaurant_service import RestaurantService

app = FastAPI()

# Instância global do SQLite
DATABASE = DB()

@app.post("/restaurants")
def create_restaurant(email: str, password: str, restaurant_name: str, commission: float):
    """
    API 1: Creates a single restaurant
    """   
    restaurant = Restaurant(pk=None, email=email, password=password, restaurant_name=restaurant_name, commission=commission, menu=[])

    # Valida campos
    erro = restaurant.verificar_validacoes()
    if erro:
        return erro
    
    # Verifica duplicidade
    if DATABASE.exists_restaurant(email, restaurant_name):
        return "Restaurante ou email já cadastrado."

    # Salva no banco (SQLite gera o PK)
    DATABASE.create_restaurant(restaurant)
    return f"Restaurante {restaurant.restaurant_name} cadastrado com sucesso!"


@app.post("/restaurants/menu")
def add_product(email: str, password: str, name: str, price: float):
    """
    API 2: Creates a product for a given restaurant
    """
    service = RestaurantService(email, password)

    if not service._is_authenticated():
        return "Falha no login: restaurante não encontrado."

    return service.add_product(name, price)


@app.delete("/restaurants/menu")
def delete_product(email: str, password: str, product_pk: int):
    """
    API 3: Deletes a product for a given restaurant
    """
    service = RestaurantService(email, password)
    return service.delete_product(product_pk)


@app.get("/restaurants")
def get_restaurants_list():
    """
    API 4: List all restaurants sorted by commission
    """
    return DATABASE.get_restaurants()


@app.patch("/restaurants")
def update_commission(email: str, password: str, commission: float):
    """
    API 5: Updates a commission of a restaurant
    """
    service = RestaurantService(email, password)
    return service.update_commission(commission)