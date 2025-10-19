import json
import os

class Geradorpk:
    CONTADOR_PK = "database/geradorpk/pk_counter.json"

    @classmethod
    def gerador_pk(cls, nome: str) -> int:
        # Se o arquivo não existir, cria com dicionário vazio
        if not os.path.exists(cls.CONTADOR_PK) or os.path.getsize(cls.CONTADOR_PK) == 0:
            with open(cls.CONTADOR_PK, "w") as arquivo:
                json.dump({}, arquivo)

        # Lê os contadores existentes
        with open(cls.CONTADOR_PK, "r") as arquivo:
            contador = json.load(arquivo)

        # Pega o último pk usado ou começa do zero
        ultimo_pk = contador.get(nome, 0)
        novo_pk = ultimo_pk + 1

        # Atualiza o contador e salva
        contador[nome] = novo_pk
        with open(cls.CONTADOR_PK, "w") as arquivo:
            json.dump(contador, arquivo, indent=4)

        return novo_pk