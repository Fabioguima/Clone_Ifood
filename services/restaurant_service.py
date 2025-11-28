from database.db import DB
from models.restaurant import Restaurant


class RestaurantService:
    def __init__(self, email: str, password: str):
        self.db = DB()
        self.email = email.lower().strip()
        self.password = password
        self.restaurant: Restaurant | None = self.db.login(self.email, self.password) # Login com as informações passadas


    def _is_authenticated(self) -> bool: # Verifica se o restaurante existe no DB
        return self.restaurant is not None


    def _validate_product(self, name: str, price: float): # Validação do Produto
        name = name.strip()

        if len(name) <= 4:
            return "O nome do produto deve ter mais de 4 caracteres."
        if price <= 0:
            return "O preço do produto deve ser maior que zero."

        return None


    def add_product(self, name: str, price: float) -> str: # Adiciona produto
        if not self._is_authenticated():
            return "Falha no login: restaurante não encontrado."

        erro = self._validate_product(name, price) # Valida nome e preço do produto
        if erro:
            return erro

        name = name.strip().lower() # Retira os espaços em branco das pontas e ganrante lowercase

        conn = self.db.get_conn() # Conexão com DB
        cur = conn.cursor()

        # Verificar duplicidade do produto
        cur.execute(
            """
            SELECT id FROM product
            WHERE LOWER(nome) = LOWER(?) AND restaurant_id = ?
            """,
            (name, self.restaurant.pk)
        )

        if cur.fetchone():  # Verifica se ao menos uma linha atende ao requisito, no caso se o produto já existe atrelado aquele Restaurante
            return f"O produto '{name}' já existe no menu."

        # Inseri o produto na tabela
        cur.execute(
            """
            INSERT INTO product (nome, preco, restaurant_id)
            VALUES (?, ?, ?)
            """,
            (name, price, self.restaurant.pk)
        )
        conn.commit() # Salva as alterações
        conn.close() # Fecha o DB

        return f"Produto '{name}' adicionado com sucesso."


    def delete_product(self, product_pk: int) -> str: # Remove produto
        if not self._is_authenticated():
            return "Falha no login: restaurante não encontrado."

        conn = self.db.get_conn() # Conexão como o DB
        cur = conn.cursor() # Envia os comandos ao SQL

        cur.execute(
            """
            SELECT nome FROM product
            WHERE id = ? AND restaurant_id = ?
            """,
            (product_pk, self.restaurant.pk)
        )

        row = cur.fetchone() # Verifica existencia de uma linha do comando pedido acima

        if not row:
            return "Produto não encontrado."

        product_name = row["nome"]

        # Deleta o produto para o Restaurante selecionado restaurante_id = ?
        cur.execute(
            """
            DELETE FROM product
            WHERE id = ? AND restaurant_id = ?
            """,
            (product_pk, self.restaurant.pk)
        )
        conn.commit() # Salva as alterações
        conn.close() # Fecha o DB

        return f"O produto '{product_name}' foi removido com sucesso."


    def update_commission(self, commission: float) -> str: # Atualiza comissão
        if not self._is_authenticated():
            return "Falha no login: restaurante não encontrado."

        if not Restaurant._validate_commission(commission): # Valida comissão
            return "A comissão deve ser maior ou igual a 0."

        conn = self.db.get_conn()
        cur = conn.cursor()

        # Atualiza a comissão do Restaurante quando a id existir.
        cur.execute(
            """
            UPDATE restaurant
            SET commission = ?
            WHERE id = ?
            """,
            (commission, self.restaurant.pk)
        )

        conn.commit() # Salva o DB
        conn.close() # Fecha o DB

        return f"Comissão atualizada para {commission} com sucesso."