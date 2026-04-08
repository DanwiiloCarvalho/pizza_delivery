# 🍕 Pizza Delivery API

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0+-blue?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Pytest-Testing-blue?style=for-the-badge&logo=pytest" alt="Pytest">
  <img src="https://img.shields.io/badge/Celery-5.6.0-green?style=for-the-badge&logo=celery" alt="Celery">
  <img src="https://img.shields.io/badge/-RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white" alt="RabbitMQ">
</p>

O **Pizza Delivery API** é uma interface de backend robusta desenvolvida para gerenciar pedidos de uma pizzaria, permitindo o controle de usuários, produtos e status de entregas em tempo real.

---

## 🚀 Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://uvicorn.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/en/stable/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [RabbitMQ](https://www.rabbitmq.com/)

---

## 🛣️ Rotas da API

Abaixo estão listadas as principais rotas disponíveis na documentação interativa (Swagger UI).

### Autenticação (Auth)
*   `POST api/auth/create_account` - Criação de uma nova conta de usuário.
*   `POST api/auth/login` - Autenticação de usuário e geração de token JWT.
*   `POST api/auth/refresh` - Gera um novo access token para utilização das rotas protegidas.

### Pedidos (Orders)
*   `GET api/orders/` - Lista todos os pedidos realizados (Acesso restrito a administradores).
*   `GET /orders/{order_id}` - Busca detalhes de um pedido específico pelo ID.
*   `POST api/orders/` - Realiza um novo pedido de pizza.
*   `POST api/orders/{order_id}/items` - Adiciona um novo item ao pedido.
*   `DELETE api/orders/{order_id}/items/{item_id}` - Remove um item de um pedido, especificando o ID do pedido e do item.
*   `DELETE api/orders/{order_id}` - Remove um pedido.
*   `PATCH api/orders/{order_id}/cancel` - Cancela um pedido específico pelo ID.
*   `PATCH api/orders/{order_id}/complete` - Finaliza um pedido específico pelo ID.

### Usuários (Users)
*   `GET api/users/{user_id}/orders` - Lista todos os pedidos de um usuário.