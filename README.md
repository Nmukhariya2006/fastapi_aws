# FastAPI Todo API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_ECS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

A lightweight CRUD REST API for managing todo items, built with **FastAPI**, **SQLAlchemy**, and **SQLite**. Includes full containerization via **Docker** and deployment configurations for **AWS ECS (Fargate)**.

---

## Features

- **CRUD Operations**: Full RESTful endpoints for creating, reading, updating, and deleting todo items.
- **Interactive API Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Database Abstraction**: Uses SQLAlchemy ORM for easy database switching (e.g., SQLite to PostgreSQL).
- **Containerization**: Included `Dockerfile` and `docker-compose.yml` with persistent volume mounting.
- **Production-Ready Deployment**: Pre-configured task definition for AWS ECS Fargate deployment.

---

## Project Structure

```text
fastapi_todos/
├── app/
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy engine & session setup
│   ├── models.py           # Database table definitions
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── crud.py            # Database read/write functions
│   └── main.py            # FastAPI application & routes
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── ecs-task-definition.json
├── README.md
└── requirements.txt
