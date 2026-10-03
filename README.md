Todos API
A small CRUD API for managing todos, built with FastAPI, SQLAlchemy, and SQLite. Includes a Dockerfile for running it in Docker or deploying it to AWS ECS.

Project structure
fastapi_todos/
├── app/
│   ├── __init__.py
│   ├── database.py      # SQLAlchemy engine/session setup
│   ├── models.py        # Todo table definition
│   ├── schemas.py       # Pydantic request/response models
│   ├── crud.py          # Database read/write functions
│   └── main.py          # FastAPI routes
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── ecs-task-definition.json
└── README.md
Data model
Each todo has:

Field	Type	Notes
id	int	Auto-generated
title	string	Required
description	string	Optional
completed	bool	Defaults to false
created_at	datetime	Set automatically
updated_at	datetime	Updated automatically on edits
API endpoints
Method	Path	Description
GET	/health	Health check
POST	/todos/	Create a todo
GET	/todos/	List todos (skip, limit query params)
GET	/todos/{id}	Get one todo
PUT	/todos/{id}	Update a todo (partial)
DELETE	/todos/{id}	Delete a todo
Once the app is running, interactive docs are available at /docs (Swagger UI) and /redoc.

Run it locally (no Docker)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
The API is now at http://localhost:8000. The SQLite file is created automatically at ./data/todos.db.

Quick test:

curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2% please"}'

curl http://localhost:8000/todos/
Run it with Docker
docker build -t fastapi-todos .
docker run -d -p 8000:8000 -v "$(pwd)/data:/app/data" --name fastapi-todos fastapi-todos
Or with Docker Compose:

docker compose up --build
The -v ./data:/app/data volume keeps your todos across container restarts — without it, the SQLite file lives only inside the container's writable layer and is lost when the container is removed.

Deploying to AWS ECS
This ships as a single stateless container, so it works with either ECS launch type. Steps below use Fargate since it needs no EC2 management.

Create an ECR repository and push the image

aws ecr create-repository --repository-name fastapi-todos

aws ecr get-login-password --region <REGION> | \
  docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com

docker build -t fastapi-todos .
docker tag fastapi-todos:latest <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/fastapi-todos:latest
docker push <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/fastapi-todos:latest
Register the task definition

Edit ecs-task-definition.json, replacing <ACCOUNT_ID> and <REGION>, then:

aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
(awslogs-create-group: true lets ECS create the CloudWatch log group automatically, so no separate step is needed for that.)

Create a cluster and service

aws ecs create-cluster --cluster-name fastapi-todos-cluster

aws ecs create-service \
  --cluster fastapi-todos-cluster \
  --service-name fastapi-todos-service \
  --task-definition fastapi-todos \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[<SECURITY_GROUP_ID>],assignPublicIp=ENABLED}"
The security group needs an inbound rule allowing TCP port 8000 (or put an Application Load Balancer in front and point it at the container's port 8000, which is the usual setup for anything beyond quick testing).

Confirm it's healthy — check the ECS service events in the console, or once you have a reachable IP/DNS name: curl http://<address>:8000/health.

A note on persistence
SQLite stores its data as a single file. On ECS Fargate, a task's local disk is ephemeral: it's wiped whenever the task restarts, redeploys, or scales past one instance. That's fine for trying things out, but for anything you need to keep, do one of:

Mount an EFS volume at /app/data in the task definition, so the file survives restarts. Note that SQLite isn't designed for multiple writers over a network filesystem, so keep desired-count at 1 if you go this route.
Swap in a real database (e.g., RDS Postgres) for multi-instance or production use. Since the app talks to the database only through SQLAlchemy, this just means changing the DATABASE_URL environment variable (e.g., postgresql://user:pass@host/dbname) and adding psycopg2-binary to requirements.txt — no application code changes needed.
Configuration
Env var	Default	Purpose
DATABASE_URL	sqlite:///./data/todos.db	SQLAlchemy