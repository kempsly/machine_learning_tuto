# Docker Complete Tutorial
> **Master Docker from scratch** — containers, images, volumes, networks, Docker Compose, and production deployment  
> Written for data scientists and ML engineers

---

## Table of Contents

- [Docker Complete Tutorial](#docker-complete-tutorial)
  - [Table of Contents](#table-of-contents)
  - [1. What is Docker?](#1-what-is-docker)
    - [The Problem Docker Solves](#the-problem-docker-solves)
    - [Docker vs Virtual Machines](#docker-vs-virtual-machines)
    - [Key Benefits for Data Scientists](#key-benefits-for-data-scientists)
  - [2. Installation](#2-installation)
    - [Mac](#mac)
    - [Linux (Ubuntu)](#linux-ubuntu)
    - [Verify Installation](#verify-installation)
  - [3. Core Concepts](#3-core-concepts)
    - [Image](#image)
    - [Container](#container)
    - [Registry](#registry)
    - [Volume](#volume)
    - [Network](#network)
  - [4. Your First Container](#4-your-first-container)
    - [Port Mapping Explained](#port-mapping-explained)
  - [5. Docker Images](#5-docker-images)
  - [6. Dockerfile — Build Your Own Image](#6-dockerfile--build-your-own-image)
    - [Basic Dockerfile](#basic-dockerfile)
    - [Build and Run](#build-and-run)
    - [ENTRYPOINT vs CMD](#entrypoint-vs-cmd)
  - [7. Dockerfile Best Practices](#7-dockerfile-best-practices)
    - [Layer Caching — The Most Important Optimization](#layer-caching--the-most-important-optimization)
    - [Minimize Image Size](#minimize-image-size)
    - [.dockerignore File](#dockerignore-file)
  - [8. Volumes — Persisting Data](#8-volumes--persisting-data)
  - [9. Networks](#9-networks)
  - [10. Docker Compose](#10-docker-compose)
    - [Basic docker-compose.yml](#basic-docker-composeyml)
    - [Docker Compose Commands](#docker-compose-commands)
    - [Minimal docker-compose.yml for ML Project](#minimal-docker-composeyml-for-ml-project)
  - [11. Environment Variables \& Secrets](#11-environment-variables--secrets)
    - [Never Do This](#never-do-this)
  - [12. Multi-Stage Builds](#12-multi-stage-builds)
  - [13. Dockerizing a FastAPI App](#13-dockerizing-a-fastapi-app)
    - [Project Structure](#project-structure)
    - [requirements.txt](#requirementstxt)
    - [main.py](#mainpy)
    - [Dockerfile](#dockerfile)
    - [docker-compose.yml](#docker-composeyml)
    - [Build and Run](#build-and-run-1)
  - [14. Dockerizing a ML Pipeline](#14-dockerizing-a-ml-pipeline)
  - [15. Pushing to Docker Hub](#15-pushing-to-docker-hub)
  - [16. Docker for Production](#16-docker-for-production)
    - [Health Checks](#health-checks)
    - [Resource Limits](#resource-limits)
    - [Logging](#logging)
  - [17. Useful Commands Reference](#17-useful-commands-reference)
  - [18. Cheat Sheet](#18-cheat-sheet)
  - [Learning Path](#learning-path)

---

## 1. What is Docker?

Docker is a platform that packages your application and all its dependencies into a **container** — a lightweight, isolated, portable unit that runs the same way on any machine.

### The Problem Docker Solves

Without Docker:
```
Developer A runs Python 3.9 + pandas 1.3 → works fine
Developer B runs Python 3.11 + pandas 2.0 → breaks
Production server runs Python 3.8 → breaks differently
```

With Docker:
```
Everyone runs the same container → works everywhere
"It works on my machine" becomes "It works in my container"
```

### Docker vs Virtual Machines

| Feature | Virtual Machine | Docker Container |
|---|---|---|
| Startup time | Minutes | Seconds |
| Size | GBs | MBs |
| OS | Full OS per VM | Shares host OS kernel |
| Isolation | Complete | Process-level |
| Performance | Slower | Near-native |
| Portability | Limited | Excellent |

### Key Benefits for Data Scientists

- **Reproducibility** — same Python version, same library versions, every time
- **Isolation** — no more dependency conflicts between projects
- **Portability** — build locally, deploy to any cloud
- **Collaboration** — teammates get the exact same environment instantly

---

## 2. Installation

### Mac

```bash
# Option 1 — Docker Desktop (recommended, includes GUI)
# Download from https://www.docker.com/products/docker-desktop/
# Install .dmg file and follow instructions

# Option 2 — Homebrew
brew install --cask docker

# Start Docker Desktop from Applications
# verify installation
docker --version
docker compose version
```

### Linux (Ubuntu)

```bash
# update package index
sudo apt-get update

# install dependencies
sudo apt-get install ca-certificates curl gnupg

# add Docker's GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# run without sudo
sudo usermod -aG docker $USER
newgrp docker

# verify
docker --version
```

### Verify Installation

```bash
docker --version          # Docker version 24.x.x
docker compose version    # Docker Compose version 2.x.x
docker run hello-world    # pulls and runs a test container
```

---

## 3. Core Concepts

Before writing any commands, understand these five concepts.

### Image

An **image** is a read-only blueprint for creating containers. It contains:
- The operating system layer (e.g. Ubuntu, Alpine)
- Runtime (e.g. Python 3.10)
- Libraries (e.g. pandas, fastapi)
- Your application code
- Configuration

Images are built from a `Dockerfile` and stored in registries like Docker Hub.

### Container

A **container** is a running instance of an image. The relationship is:
```
Image  →  Container
(blueprint)  →  (running instance)

Just like:
Class  →  Object  (in Python)
Recipe →  Cake    (in cooking)
```

You can run many containers from the same image simultaneously.

### Registry

A **registry** is a storage service for images. 
- **Docker Hub** — public registry (hub.docker.com)
- **AWS ECR** — Amazon's private registry
- **GitHub Container Registry** — GitHub's registry
- **Self-hosted** — your own private registry

### Volume

A **volume** is a way to persist data outside the container. When a container stops, its data is gone — volumes solve this by mapping a folder inside the container to a folder on your host machine.

### Network

A **network** allows containers to communicate with each other. By default containers are isolated — networks connect them.

---

## 4. Your First Container

```bash
# pull an image from Docker Hub
docker pull ubuntu:22.04

# run a container interactively
# -it = interactive terminal
# ubuntu:22.04 = image name:tag
docker run -it ubuntu:22.04 bash

# you are now inside the container
ls
echo "I am inside a container"
exit    # leave the container

# run a container and remove it when done
docker run --rm ubuntu:22.04 echo "hello from container"

# run a container in the background (detached)
# -d = detached mode
# --name = give it a name
docker run -d --name my_container ubuntu:22.04 sleep 3600

# check running containers
docker ps

# check all containers (including stopped)
docker ps -a

# stop a container
docker stop my_container

# remove a container
docker rm my_container

# run nginx web server (real world example)
# -p 8080:80 = map host port 8080 to container port 80
docker run -d -p 8080:80 --name webserver nginx

# open http://localhost:8080 in your browser → nginx welcome page
docker stop webserver
docker rm webserver
```

### Port Mapping Explained

```
Host machine          Container
port 8080     →→→     port 80

-p HOST_PORT:CONTAINER_PORT
-p 8080:80
-p 8000:8000
-p 5432:5432    (PostgreSQL)
-p 6379:6379    (Redis)
```

---

## 5. Docker Images

```bash
# ── Searching and pulling images ─────────────────────────────

# search Docker Hub
docker search python

# pull specific version (always use specific tags in production)
docker pull python:3.10-slim       # slim = minimal image
docker pull python:3.10-alpine     # alpine = even smaller (musl libc)
docker pull python:3.10            # full image

# list local images
docker images
docker image ls

# image details
docker inspect python:3.10-slim

# remove an image
docker rmi python:3.10
docker image rm python:3.10

# remove all unused images (free disk space)
docker image prune -a

# ── Image tags ────────────────────────────────────────────────
# format: image_name:tag
# python:3.10-slim
# python:latest          ← avoid in production — always pin versions
# ubuntu:22.04
# postgres:15.2
# nginx:1.25-alpine

# ── Useful base images for ML ─────────────────────────────────
# python:3.10-slim          → lightweight Python
# python:3.10               → full Python with build tools
# jupyter/scipy-notebook    → Jupyter with scientific stack
# tensorflow/tensorflow:2.13.0  → TensorFlow with GPU support
# pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime  → PyTorch with CUDA
```

---

## 6. Dockerfile — Build Your Own Image

A `Dockerfile` is a text file with instructions to build a custom image.

### Basic Dockerfile

```dockerfile
# Dockerfile

# ── Base image ────────────────────────────────────────────────
# FROM = start from this base image
# always pin the exact version for reproducibility
FROM python:3.10-slim

# ── Metadata ──────────────────────────────────────────────────
# LABEL = add metadata to the image
LABEL maintainer="kempsly@example.com"
LABEL version="1.0"
LABEL description="ML pipeline container"

# ── Environment variables ─────────────────────────────────────
# ENV = set environment variables inside the container
ENV PYTHONDONTWRITEBYTECODE=1    # don't write .pyc files
ENV PYTHONUNBUFFERED=1           # don't buffer stdout/stderr

# ── Working directory ─────────────────────────────────────────
# WORKDIR = set the working directory inside the container
# all subsequent commands run from this directory
WORKDIR /app

# ── Copy files ────────────────────────────────────────────────
# COPY source destination
# copy requirements first (for layer caching — explained below)
COPY requirements.txt .

# ── Install dependencies ──────────────────────────────────────
# RUN = execute a command during build
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of your code
COPY . .

# ── Expose port ───────────────────────────────────────────────
# EXPOSE = document which port the app uses (informational)
# does NOT actually publish the port — use -p flag for that
EXPOSE 8000

# ── Start command ─────────────────────────────────────────────
# CMD = command to run when container starts
# only one CMD per Dockerfile (last one wins)
CMD ["python", "app.py"]
```

### Build and Run

```bash
# build the image
# -t = tag (name:version)
# . = build context (current directory — where Dockerfile is)
docker build -t my-ml-app:1.0 .

# build with no cache (force rebuild everything)
docker build --no-cache -t my-ml-app:1.0 .

# run the container
docker run -p 8000:8000 my-ml-app:1.0

# run with environment variable
docker run -p 8000:8000 -e API_KEY=secret my-ml-app:1.0

# run interactively to debug
docker run -it my-ml-app:1.0 bash
```

### ENTRYPOINT vs CMD

```dockerfile
# CMD — default command, can be overridden at runtime
CMD ["python", "app.py"]

# run with override:
# docker run my-app python other_script.py  ← overrides CMD

# ENTRYPOINT — fixed command, cannot be overridden easily
ENTRYPOINT ["python", "app.py"]

# ENTRYPOINT + CMD — entrypoint is fixed, CMD provides default args
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run my-app other_script.py  ← runs: python other_script.py
```

---

## 7. Dockerfile Best Practices

### Layer Caching — The Most Important Optimization

Docker builds images in layers. Each instruction creates a layer. If a layer hasn't changed, Docker reuses the cached version — making rebuilds very fast.

```dockerfile
# BAD — copies everything first, then installs
# any code change invalidates the pip install layer
FROM python:3.10-slim
COPY . .
RUN pip install -r requirements.txt   # runs every time ANY file changes

# GOOD — copy requirements first, install, then copy code
# pip install layer is only invalidated when requirements.txt changes
FROM python:3.10-slim
COPY requirements.txt .
RUN pip install -r requirements.txt   # cached unless requirements change
COPY . .                              # code changes don't affect pip layer
```

### Minimize Image Size

```dockerfile
# Use slim or alpine base images
FROM python:3.10-slim          # ~150MB
# vs
FROM python:3.10               # ~900MB

# Combine RUN commands to reduce layers
# BAD — creates 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# GOOD — one layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use --no-cache-dir with pip
RUN pip install --no-cache-dir -r requirements.txt

# Remove unnecessary files
RUN pip install --no-cache-dir pandas && \
    find /usr/local/lib/python3.10 -name "*.pyc" -delete
```

### .dockerignore File

Like `.gitignore` but for Docker — prevents unnecessary files from being sent to the build context.

```
# .dockerignore

# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/

# Virtual environments
venv/
.venv/
env/

# Data and models (usually too large)
data/
*.csv
*.pkl
*.h5
models/

# Git
.git/
.gitignore

# Environment files
.env
.env.*

# IDE
.vscode/
.idea/

# Jupyter checkpoints
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose.yml
```

---

## 8. Volumes — Persisting Data

Without volumes, data created inside a container disappears when the container stops.

```bash
# ── Named volumes (managed by Docker) ────────────────────────

# create a named volume
docker volume create my_data

# list volumes
docker volume ls

# run container with volume
# -v volume_name:container_path
docker run -v my_data:/app/data my-ml-app

# inspect volume
docker volume inspect my_data

# remove volume
docker volume rm my_data

# remove all unused volumes
docker volume prune

# ── Bind mounts (map host folder to container) ────────────────
# useful for development — changes on host reflect in container immediately
# -v /host/path:/container/path

# map current directory to /app in container
docker run -v $(pwd):/app my-ml-app

# map specific folder
docker run -v /Users/kempsly/data:/app/data my-ml-app

# ── Read-only mount ───────────────────────────────────────────
# :ro = read-only — container cannot write to this path
docker run -v /Users/kempsly/data:/app/data:ro my-ml-app

# ── Practical example — ML model persistence ──────────────────
# train a model and save it to a volume
docker run \
  -v ml_models:/app/models \
  -v $(pwd)/data:/app/data:ro \
  my-ml-trainer python train.py

# the trained model is now in the ml_models volume
# use it in another container
docker run \
  -v ml_models:/app/models:ro \
  -p 8000:8000 \
  my-ml-api
```

---

## 9. Networks

Networks allow containers to communicate with each other.

```bash
# ── Default networks ──────────────────────────────────────────
# bridge  = default network for containers on same host
# host    = container uses host network directly (Linux only)
# none    = no networking

# list networks
docker network ls

# ── Create a custom network ───────────────────────────────────
docker network create ml_network

# run containers on the same network
# containers can reach each other by container name
docker run -d --name db --network ml_network postgres:15
docker run -d --name api --network ml_network -p 8000:8000 my-api

# now inside the api container:
# you can connect to the database using hostname "db"
# e.g. postgresql://db:5432/mydb

# inspect network
docker network inspect ml_network

# remove network
docker network rm ml_network

# connect existing container to network
docker network connect ml_network my_container

# disconnect
docker network disconnect ml_network my_container
```

---

## 10. Docker Compose

Docker Compose lets you define and run **multi-container applications** with a single YAML file. Instead of running multiple `docker run` commands, you define everything in `docker-compose.yml`.

### Basic docker-compose.yml

```yaml
# docker-compose.yml

version: "3.9"    # compose file version

services:

  # ── FastAPI application ──────────────────────────────────────
  api:
    build:
      context: .            # build from Dockerfile in current directory
      dockerfile: Dockerfile
    container_name: finsaight_api
    ports:
      - "8000:8000"         # host:container
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
      - DATABASE_URL=postgresql://user:password@db:5432/finsaight
    volumes:
      - ./models:/app/models    # persist models
      - ./logs:/app/logs        # persist logs
    depends_on:
      - db                  # wait for db to start first
      - redis
    networks:
      - ml_network
    restart: unless-stopped   # restart automatically unless manually stopped

  # ── PostgreSQL database ───────────────────────────────────────
  db:
    image: postgres:15.2
    container_name: finsaight_db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=finsaight
    volumes:
      - postgres_data:/var/lib/postgresql/data   # persist DB data
    ports:
      - "5432:5432"
    networks:
      - ml_network
    restart: unless-stopped

  # ── Redis cache ───────────────────────────────────────────────
  redis:
    image: redis:7.2-alpine
    container_name: finsaight_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - ml_network
    restart: unless-stopped

  # ── MLflow tracking server ────────────────────────────────────
  mlflow:
    image: python:3.10-slim
    container_name: finsaight_mlflow
    command: >
      bash -c "pip install mlflow && 
               mlflow server --host 0.0.0.0 --port 5000 
               --backend-store-uri postgresql://user:password@db:5432/mlflow
               --default-artifact-root /mlflow/artifacts"
    ports:
      - "5000:5000"
    volumes:
      - mlflow_artifacts:/mlflow/artifacts
    depends_on:
      - db
    networks:
      - ml_network

# ── Named volumes ─────────────────────────────────────────────
volumes:
  postgres_data:
  redis_data:
  mlflow_artifacts:

# ── Networks ──────────────────────────────────────────────────
networks:
  ml_network:
    driver: bridge
```

### Docker Compose Commands

```bash
# start all services (build if needed)
docker compose up

# start in background (detached)
docker compose up -d

# start and force rebuild images
docker compose up --build

# stop all services
docker compose down

# stop and remove volumes (WARNING: deletes all data)
docker compose down -v

# view logs
docker compose logs
docker compose logs api           # logs for specific service
docker compose logs -f api        # follow logs in real time

# check status
docker compose ps

# execute command in running service
docker compose exec api bash
docker compose exec db psql -U user -d finsaight

# scale a service (run multiple instances)
docker compose up --scale api=3

# rebuild a specific service
docker compose build api
docker compose up -d --no-deps api   # restart only api without restarting deps
```

### Minimal docker-compose.yml for ML Project

```yaml
# docker-compose.yml — minimal ML project setup

version: "3.9"

services:

  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env              # load all env vars from .env file
    volumes:
      - .:/app            # bind mount for development (live reload)
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 11. Environment Variables & Secrets

```bash
# ── Method 1 — inline with -e flag ────────────────────────────
docker run -e API_KEY=secret -e DEBUG=true my-app

# ── Method 2 — .env file ──────────────────────────────────────
# create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
LANGSMITH_API_KEY=your_langsmith_key
DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=false
EOF

# pass .env file to docker run
docker run --env-file .env my-app

# in docker-compose.yml — reference .env automatically
# docker compose reads .env from same directory by default
```

```yaml
# docker-compose.yml

services:
  api:
    build: .
    # Method A — load entire .env file
    env_file:
      - .env

    # Method B — reference specific variables from shell environment
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DATABASE_URL=${DATABASE_URL}

    # Method C — hardcode non-sensitive values
    environment:
      - DEBUG=false
      - LOG_LEVEL=info
      - PORT=8000
```

### Never Do This

```dockerfile
# NEVER hardcode secrets in Dockerfile
ENV API_KEY=sk-abc123          # visible in image history
ENV DATABASE_PASSWORD=secret   # anyone with the image can see this

# check image history
docker history my-app          # shows all ENV values
```

---

## 12. Multi-Stage Builds

Multi-stage builds create smaller production images by separating the build environment from the runtime environment.

```dockerfile
# Dockerfile.multistage

# ── Stage 1: Builder ──────────────────────────────────────────
# uses full Python image with build tools
FROM python:3.10 AS builder

WORKDIR /app

# install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Stage 2: Production ───────────────────────────────────────
# uses slim image — no build tools needed at runtime
FROM python:3.10-slim AS production

WORKDIR /app

# copy only the installed packages from builder stage
# not the full Python installation with compilers etc.
COPY --from=builder /root/.local /root/.local

# copy application code
COPY . .

# make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# build production image
docker build -f Dockerfile.multistage -t my-app:prod .

# compare sizes
docker images | grep my-app
# my-app:prod   →  ~200MB
# my-app:dev    →  ~900MB
```

---

## 13. Dockerizing a FastAPI App

### Project Structure

```
finsaight/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── requirements.txt
└── main.py
```

### requirements.txt

```
fastapi==0.111.0
uvicorn==0.30.0
langchain==0.2.0
langchain-groq==0.1.0
langchain-community==0.2.0
python-dotenv==1.0.0
pydantic==2.7.0
```

### main.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Fins'AIght API")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "ok", "service": "finsaight-api"}

@app.post("/ask")
def ask(request: QueryRequest):
    return {"question": request.question, "answer": "placeholder"}
```

### Dockerfile

```dockerfile
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY . .

# expose FastAPI port
EXPOSE 8000

# start uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: "3.9"

services:
  api:
    build: .
    container_name: finsaight_api
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### Build and Run

```bash
# build and start
docker compose up --build

# test the API
curl http://localhost:8000/
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'

# open Swagger UI
# http://localhost:8000/docs
```

---

## 14. Dockerizing a ML Pipeline

```dockerfile
# Dockerfile for ML training + serving pipeline

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install system dependencies for ML libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# create directories for data and models
RUN mkdir -p /app/data /app/models /app/logs

EXPOSE 8000

# default command — can be overridden
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml for full ML stack

version: "3.9"

services:

  # training service
  trainer:
    build: .
    command: python train.py
    volumes:
      - ./data:/app/data:ro          # read-only data
      - ml_models:/app/models        # write trained models
      - mlflow_data:/app/mlruns      # mlflow tracking
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    depends_on:
      - mlflow
    profiles:
      - training                     # only runs with: docker compose --profile training up

  # serving service
  api:
    build: .
    command: uvicorn api:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - ml_models:/app/models:ro     # read-only access to models
    env_file:
      - .env
    restart: unless-stopped

  # MLflow tracking
  mlflow:
    image: python:3.10-slim
    command: >
      bash -c "pip install mlflow &&
               mlflow server --host 0.0.0.0 --port 5000
               --backend-store-uri sqlite:///mlflow.db
               --default-artifact-root /mlflow/artifacts"
    ports:
      - "5000:5000"
    volumes:
      - mlflow_data:/mlflow

volumes:
  ml_models:
  mlflow_data:
```

```bash
# train the model
docker compose --profile training up trainer

# serve the model
docker compose up api

# view MLflow UI
# http://localhost:5000
```

---

## 15. Pushing to Docker Hub

```bash
# ── Create account at hub.docker.com first ────────────────────

# login to Docker Hub
docker login
# enter your Docker Hub username and password

# tag your image for Docker Hub
# format: username/repository:tag
docker tag my-ml-app:1.0 kempsly/finsaight-api:1.0
docker tag my-ml-app:1.0 kempsly/finsaight-api:latest

# push to Docker Hub
docker push kempsly/finsaight-api:1.0
docker push kempsly/finsaight-api:latest

# pull from Docker Hub (anywhere in the world)
docker pull kempsly/finsaight-api:1.0

# ── Automate with GitHub Actions ──────────────────────────────
# .github/workflows/docker.yml
```

```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: kempsly/finsaight-api:latest
```

---

## 16. Docker for Production

### Health Checks

```dockerfile
# Dockerfile with health check
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# health check — Docker will ping this endpoint
# --interval = check every 30s
# --timeout  = fail if no response in 10s
# --retries  = mark unhealthy after 3 failures
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml with health check
services:
  api:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s    # give container 10s to start before checking
```

### Resource Limits

```yaml
# docker-compose.yml with resource limits
services:
  api:
    build: .
    deploy:
      resources:
        limits:
          cpus: "2.0"        # max 2 CPU cores
          memory: 4G         # max 4GB RAM
        reservations:
          cpus: "0.5"        # guaranteed 0.5 CPU cores
          memory: 1G         # guaranteed 1GB RAM
```

### Logging

```yaml
services:
  api:
    build: .
    logging:
      driver: "json-file"
      options:
        max-size: "100m"     # max log file size
        max-file: "5"        # keep 5 rotated log files
```

---

## 17. Useful Commands Reference

```bash
# ── Container lifecycle ───────────────────────────────────────
docker run <image>                    # create and start container
docker start <container>              # start stopped container
docker stop <container>               # graceful stop (SIGTERM)
docker kill <container>               # force stop (SIGKILL)
docker restart <container>            # stop then start
docker rm <container>                 # remove stopped container
docker rm -f <container>              # force remove running container

# ── Container inspection ──────────────────────────────────────
docker ps                             # running containers
docker ps -a                          # all containers
docker logs <container>               # view logs
docker logs -f <container>            # follow logs
docker logs --tail 100 <container>    # last 100 lines
docker inspect <container>            # detailed JSON info
docker stats                          # live CPU/memory usage
docker stats <container>              # stats for one container
docker top <container>                # running processes inside

# ── Exec into container ───────────────────────────────────────
docker exec -it <container> bash      # open bash shell
docker exec -it <container> sh        # open sh (for alpine)
docker exec <container> python script.py  # run a script

# ── Image management ──────────────────────────────────────────
docker build -t name:tag .            # build image
docker images                         # list images
docker rmi <image>                    # remove image
docker image prune                    # remove dangling images
docker image prune -a                 # remove all unused images
docker history <image>                # show image layers
docker inspect <image>                # detailed image info

# ── System cleanup ────────────────────────────────────────────
docker system df                      # disk usage
docker system prune                   # remove stopped containers, unused networks, dangling images
docker system prune -a                # also remove unused images
docker system prune -a --volumes      # also remove volumes (DANGEROUS)

# ── Volume management ─────────────────────────────────────────
docker volume create <name>
docker volume ls
docker volume inspect <name>
docker volume rm <name>
docker volume prune

# ── Network management ────────────────────────────────────────
docker network create <name>
docker network ls
docker network inspect <name>
docker network rm <name>
docker network connect <network> <container>
docker network disconnect <network> <container>

# ── Copy files ────────────────────────────────────────────────
docker cp file.txt <container>:/app/  # host → container
docker cp <container>:/app/file.txt . # container → host

# ── Docker Compose ────────────────────────────────────────────
docker compose up -d                  # start all services detached
docker compose down                   # stop and remove containers
docker compose down -v                # also remove volumes
docker compose ps                     # status
docker compose logs -f                # follow all logs
docker compose exec <service> bash    # exec into service
docker compose build                  # rebuild images
docker compose pull                   # pull latest images
docker compose restart <service>      # restart one service
```

---

## 18. Cheat Sheet

```bash
# ── Quick reference ───────────────────────────────────────────

# run container
docker run -d -p 8000:8000 --name myapp --env-file .env myimage:1.0

# build image
docker build -t myimage:1.0 .

# shell into running container
docker exec -it myapp bash

# view logs
docker logs -f myapp

# stop and remove
docker stop myapp && docker rm myapp

# cleanup everything
docker system prune -a

# ── Dockerfile template ───────────────────────────────────────
# FROM python:3.10-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ── docker-compose.yml template ───────────────────────────────
# version: "3.9"
# services:
#   api:
#     build: .
#     ports: ["8000:8000"]
#     env_file: [.env]
#     volumes: [./logs:/app/logs]
#     restart: unless-stopped

# ── Port mappings for common services ────────────────────────
# FastAPI / Uvicorn  →  8000:8000
# Streamlit          →  8501:8501
# MLflow             →  5000:5000
# PostgreSQL         →  5432:5432
# Redis              →  6379:6379
# Nginx              →  80:80 / 443:443
# Jupyter            →  8888:8888

# ── Key flags ─────────────────────────────────────────────────
# -d          detached (background)
# -it         interactive terminal
# -p          port mapping host:container
# -v          volume mount host:container
# -e          environment variable
# --env-file  load .env file
# --name      container name
# --rm        auto-remove when stopped
# --network   connect to network
# --no-cache  build without cache
```

---

## Learning Path

```
Cell 1-4   → Understand concepts + run first container
Cell 5     → Pull and manage images
Cell 6-7   → Write your first Dockerfile
Cell 8-9   → Add volumes and networks
Cell 10    → Docker Compose for multi-service apps
Cell 11    → Manage secrets properly
Cell 12    → Multi-stage builds for production
Cell 13    → Dockerize your FastAPI app  ← most important for Natixis
Cell 14    → Dockerize your ML pipeline
Cell 15    → Push to Docker Hub
Cell 16    → Production hardening
```

---

*Docker docs: https://docs.docker.com*  
*Docker Hub: https://hub.docker.com*  
*Docker Compose docs: https://docs.docker.com/compose*  
*Play with Docker (browser sandbox): https://labs.play-with-docker.com*
