from typing import List

class Restaurant:
    def __init__(
        self,
        pk: int | None,
        email: str,
        password: str,
        restaurant_name: str,
        commission: float,
        menu: List[dict] | None = None
    ):
        # SQLite controla o PK
        self.pk = pk
        self.email = email.strip()
        self.password = password
        self.restaurant_name = restaurant_name.strip()
        self.commission = commission
        self.menu = menu or []

    def _verifica_email(self) -> bool: # Valida email
        email = self.email.lower()

        # Apenas uma @
        if "@" not in email or email.count("@") != 1:
            return False

        usuario, dominio_extensao = email.split("@")

        # Checar se tem exatamente um "."
        if "." not in dominio_extensao or dominio_extensao.count(".") != 1:
            return False

        dominio, extensao = dominio_extensao.split(".")

        # Partes vazias são inválidas
        if not usuario or not dominio or not extensao:
            return False

        # Usuário e domínio precisam ser alfanuméricos
        if not usuario.replace(".", "").isalnum():
            return False

        if not dominio.replace(".", "").isalnum():
            return False

        # Extensão deve ser só letras
        if not extensao.isalpha():
            return False

        return True


    def _verifica_senha(self) -> tuple[bool, str | None]: # Valida senha
        senha = self.password

        if len(senha) < 5:
            return False, "Senha com menos de 5 caracteres"
        if not any(c.isupper() for c in senha):
            return False, "A senha não contém letra maiúscula"
        if not any(c.islower() for c in senha):
            return False, "A senha não contém letra minúscula"
        if not any(c.isdigit() for c in senha):
            return False, "A senha não contém número"

        return True, None


    @staticmethod
    def _validate_commission(commission: float) -> bool: # Valida Comissão
        try:
            return float(commission) >= 0
        except:
            return False


    def _verifica_nome(self) -> bool: # Valida tamanho do nome Restaurante
        return len(self.restaurant_name) > 10


    def verificar_validacoes(self) -> str | None: # Validação geral

        if not self._validate_commission(self.commission): # Valida se a comissão é maior ou igual a zero
            return "A comissão deve ser maior ou igual a 0."

        if not self._verifica_email(): # Valida email
            return "Email inválido."

        senha_ok, msg = self._verifica_senha() # Valida se a senha atende aos requisitos
        if not senha_ok:
            return msg

        if not self._verifica_nome(): # Valida len do nome
            return "O nome do restaurante deve ter mais de 10 caracteres."

        return None