# Clone Ifood V2.0

🍔 Clone Ifood

Este projeto é uma simulação didática do funcionamento básico de um sistema de delivery, inspirado no modelo do iFood.
Ele foi desenvolvido em Python, utilizando conceitos de Programação Orientada a Objetos (POO), persistência de dados **em SQLite** e organização modular do código.

🧠 Objetivo

O principal objetivo deste projeto é aplicar os conceitos de POO e demonstrar o funcionamento de um sistema simples de restaurantes, produtos e autenticação.
Com ele, é possível cadastrar restaurantes, fazer login, adicionar produtos ao cardápio e salvar todas as informações em um banco de dados local.

⚙️ Tecnologias Utilizadas:

- Python 3.12+
- **SQLite para armazenamento de dados**
- Extensão **"SQLite"** do VSCode para visualizar o banco de dados diretamente no editor
- Programação Orientada a Objetos (POO)
- Estrutura modular (separação entre models, database e services)

📋 Funcionalidades:

👤 **Restaurante**
Cadastro de restaurantes com:

- E-mail válido
- Senha forte (mínimo 5 caracteres, com letra maiúscula, minúscula e número)
- Nome único e padronizado em minúsculas

Login de restaurante:

- Verificação automática de duplicidade no banco SQLite

🍕 **Produto**
Adição de produtos ao menu do restaurante logado.
Validações:

- `name` precisa ter mais de 4 caracteres
- `price` deve ser maior que 0
- Não pode haver dois produtos com o mesmo nome no menu

💾 **Banco de Dados (SQLite)**
Agora todas as informações são salvas em um banco SQLite localizado em:

```
database/restaurants.db
```

A aplicação utiliza conexões independentes por operação (abrir → usar → fechar), garantindo segurança e evitando erros como `database is locked`.

▶️ Como Executar o Projeto:

```bash
1️⃣ # Instale as dependências
pip install -r requirements.txt

2️⃣ # Inicie o servidor
fastapi dev main.py

3️⃣ # Acesse no navegador
http://localhost:8000

# A documentação automática do FastAPI estará disponível em:
http://localhost:8000/docs
```

👨‍💻 **Autor**
Desenvolvido por: Fábio Guimarães
Ano: 2025
