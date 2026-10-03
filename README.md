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


## Environment Setup
# Clone repository and enter project root
cd fastapi_todos

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
# .venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

##Running the Development Server
# Start Uvicorn with auto-reload enabled
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
---
##Containerization Guide
Docker CLI
Build Image
Bash
docker build -t fastapi-todos:1.0 .

[ Client / Inbound Traffic ]
            │
            ▼
┌─────────────────────────┐
│ Application Load Balancer│ (Optional - Port 80 / 443)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Security Group (TCP 8000)│
└───────────┬─────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────┐
│ AWS ECS Cluster (Fargate Launch Type)                   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Task Definition: fastapi-todos                     │  │
│  │                                                    │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ Container: fastapi-todos                     │  │  │
│  │  │ Image: <ACCOUNT_ID>.dkr.ecr.<REGION>...      │  │  │
│  │  │ Port Binding: 8000                           │  │  │
│  │  │ Ephemeral Disk / AWS EFS Mount: /app/data    │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

# Create ECS Cluster
aws ecs create-cluster \
  --cluster-name fastapi-todos-cluster \
  --region ${AWS_REGION}

# Create Fargate Service
aws ecs create-service \
  --cluster fastapi-todos-cluster \
  --service-name fastapi-todos-service \
  --task-definition fastapi-todos \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[\"subnet-xxxxxxxxxxxxxxxxx\"],
    securityGroups=[\"sg-xxxxxxxxxxxxxxxxx\"],
    assignPublicIp=\"ENABLED\"
  }" \
  --region ${AWS_REGION}
