# Docker & Docker Compose — Complete In-Depth Tutorial
> **The most comprehensive Docker reference** — every concept, every command, every option explained in detail  
> Written for data scientists and ML engineers building production-grade systems

---

## Table of Contents

### Docker
1. [What is Docker and Why it Exists](#1-what-is-docker-and-why-it-exists)
2. [How Docker Works Internally](#2-how-docker-works-internally)
3. [Installation](#3-installation)
4. [Docker Architecture](#4-docker-architecture)
5. [Images — Complete Guide](#5-images--complete-guide)
6. [Containers — Complete Guide](#6-containers--complete-guide)
7. [Dockerfile — Every Instruction Explained](#7-dockerfile--every-instruction-explained)
8. [Building Images — All Options](#8-building-images--all-options)
9. [Volumes — Complete Guide](#9-volumes--complete-guide)
10. [Networks — Complete Guide](#10-networks--complete-guide)
11. [Environment Variables & Secrets](#11-environment-variables--secrets)
12. [Resource Management](#12-resource-management)
13. [Logging](#13-logging)
14. [Health Checks](#14-health-checks)
15. [Multi-Stage Builds](#15-multi-stage-builds)
16. [Docker Registry](#16-docker-registry)
17. [Security Best Practices](#17-security-best-practices)
18. [Debugging & Troubleshooting](#18-debugging--troubleshooting)

### Docker Compose
19. [What is Docker Compose](#19-what-is-docker-compose)
20. [docker-compose.yml — Every Field Explained](#20-docker-composeyml--every-field-explained)
21. [Services — Complete Guide](#21-services--complete-guide)
22. [Networking in Compose](#22-networking-in-compose)
23. [Volumes in Compose](#23-volumes-in-compose)
24. [Environment & Config in Compose](#24-environment--config-in-compose)
25. [Depends On & Health Checks in Compose](#25-depends-on--health-checks-in-compose)
26. [Profiles — Conditional Services](#26-profiles--conditional-services)
27. [Scaling Services](#27-scaling-services)
28. [Docker Compose Commands — All Options](#28-docker-compose-commands--all-options)
29. [Real-World Compose Examples](#29-real-world-compose-examples)
30. [Production Docker Compose](#30-production-docker-compose)
31. [Cheat Sheet](#31-cheat-sheet)

---

# PART 1 — DOCKER

---

## 1. What is Docker and Why it Exists

### The Problem Before Docker

Software development has always suffered from the "works on my machine" problem. A developer builds an application on their laptop using Python 3.9, pandas 1.3.5, and a specific version of a C library. It works perfectly. They send the code to a colleague who has Python 3.11, pandas 2.0, and a different C library version. It crashes. They deploy to a production server running Python 3.8. It crashes differently. The entire team spends hours debugging environment differences instead of building features.

The traditional solution was virtual machines — complete isolated operating systems running inside your computer. But VMs are heavy. Each one contains a full OS, uses gigabytes of disk space, takes minutes to start, and requires significant CPU and memory just to run.

### What Docker Is

Docker is a containerization platform. A container is a lightweight, isolated process that packages your application and all its dependencies — the runtime, libraries, configuration, and code — into a single portable unit. Unlike a VM, a container shares the host machine's operating system kernel and uses only the resources it actually needs.

The result is:
- A container starts in seconds, not minutes
- A container uses megabytes, not gigabytes
- A container runs identically on a developer laptop, a CI server, and a production cloud instance
- You can run dozens of containers on a single machine

### The Container vs Virtual Machine Distinction

A virtual machine virtualizes hardware. It includes a complete operating system — kernel, drivers, system libraries, everything. The hypervisor (VMware, VirtualBox, KVM) sits between the hardware and the VMs and manages resource sharing.

A container virtualizes only the application layer. It shares the host operating system's kernel. The container runtime (Docker) manages isolation using two Linux kernel features: namespaces and cgroups.

**Namespaces** provide isolation. Each container gets its own isolated view of:
- Process IDs (the container thinks its process is PID 1)
- Network interfaces and IP addresses
- Filesystem mounts
- User IDs
- Hostnames

**Cgroups** (control groups) provide resource limits. They control how much CPU, memory, and I/O each container can use.

```
Virtual Machine:                    Docker Container:
┌─────────────────────┐            ┌─────────────────────┐
│   App A             │            │   App A             │
├─────────────────────┤            ├─────────────────────┤
│   Guest OS          │            │   Libs/Deps         │
├─────────────────────┤            ├─────────────────────┤
│   Hypervisor        │            │   Docker Engine     │
├─────────────────────┤            ├─────────────────────┤
│   Host OS           │            │   Host OS + Kernel  │
├─────────────────────┤            ├─────────────────────┤
│   Hardware          │            │   Hardware          │
└─────────────────────┘            └─────────────────────┘
Size: GBs, Start: minutes          Size: MBs, Start: seconds
```

### Why Docker Matters for Data Science and ML

In machine learning, reproducibility is fundamental. An experiment that cannot be reproduced by another researcher or engineer is scientifically meaningless. Docker solves this at the infrastructure level:

- Your Jupyter notebook, your training script, your FastAPI model server — all run in exactly the same environment every time
- Your colleague gets your Docker image and runs the exact same experiment without any setup
- Your model that was trained in Python 3.10 with scikit-learn 1.3 is served in production using the exact same Python 3.10 and scikit-learn 1.3
- You can run multiple projects with conflicting dependencies on the same machine — each in its own container

---

## 2. How Docker Works Internally

### The Union Filesystem

Docker images are built in **layers**. Each instruction in a Dockerfile creates a new layer. A layer is a set of filesystem changes — files added, modified, or deleted.

These layers are stacked on top of each other using a union filesystem (typically OverlayFS on modern Linux). The result looks like a single coherent filesystem to the application running inside the container.

```
Layer 4: Your application code        ← COPY . .
Layer 3: Python dependencies          ← RUN pip install ...
Layer 2: Python runtime               ← FROM python:3.10-slim adds these
Layer 1: Slim Debian OS               ← base of python:3.10-slim
```

Each layer is content-addressed — identified by a SHA256 hash of its content. This means:
- If two images share the same base layer, Docker stores it only once
- If you rebuild an image and only the top layer changed, Docker reuses all lower layers from cache
- If you pull an image and you already have some of its layers, Docker only downloads the missing ones

### The Container Layer

When you start a container from an image, Docker adds one more layer on top — the **container layer**. This is a thin, writable layer. All changes the running container makes (creating files, modifying files, writing logs) go into this layer.

The image layers below are read-only and shared between all containers running from the same image. This is why running 100 containers from the same image doesn't require 100 copies of the image — they all share the read-only layers and each has only a thin writable layer on top.

When the container is removed, its writable layer is deleted. This is why you need volumes to persist data.

### The Docker Daemon

The Docker daemon (`dockerd`) is a background process that manages everything. It:
- Listens for Docker API requests
- Manages images, containers, volumes, and networks
- Pulls images from registries
- Starts and stops containers
- Manages the container lifecycle

The `docker` command you type in the terminal is a client that sends requests to the daemon via the Docker API (typically over a Unix socket at `/var/run/docker.sock`).

```
docker CLI  →  Docker API  →  Docker Daemon  →  containerd  →  runc  →  Container
(your terminal)              (background process)  (container runtime)  (OCI runtime)
```

---

## 3. Installation

### Mac

```bash
# Option 1 — Docker Desktop (recommended)
# Download the .dmg from https://www.docker.com/products/docker-desktop/
# Docker Desktop includes:
# - Docker Engine (the daemon)
# - Docker CLI
# - Docker Compose
# - Docker Scout (image vulnerability scanning)
# - A GUI dashboard

# Option 2 — Homebrew
brew install --cask docker

# After installation, launch Docker Desktop from Applications
# Wait for the Docker icon in the menu bar to show "Docker Desktop is running"

# verify everything works
docker --version              # Docker version 24.x.x, build ...
docker compose version        # Docker Compose version v2.x.x
docker info                   # detailed system information
docker run hello-world        # pull and run a test container
```

### Linux (Ubuntu/Debian)

```bash
# step 1 — remove old versions if any
sudo apt-get remove docker docker-engine docker.io containerd runc

# step 2 — install prerequisites
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# step 3 — add Docker's official GPG key
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# step 4 — set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# step 5 — install Docker Engine
sudo apt-get update
sudo apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# step 6 — allow running Docker without sudo
sudo usermod -aG docker $USER
newgrp docker

# step 7 — enable Docker to start on boot
sudo systemctl enable docker
sudo systemctl start docker

# verify
docker run hello-world
```

### Post-Installation Verification

```bash
docker --version          # check Docker version
docker compose version    # check Compose version
docker info               # system-wide information:
                          # - number of containers (running, stopped)
                          # - number of images
                          # - storage driver
                          # - operating system
                          # - memory, CPU count
                          # - Docker Root Dir

docker system df          # disk usage:
                          # - images: total size of all images
                          # - containers: size of container layers
                          # - volumes: size of named volumes
                          # - build cache: size of build cache
```

---

## 4. Docker Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Client (CLI)                       │
│   docker build / docker run / docker pull / docker push     │
└─────────────────────────┬───────────────────────────────────┘
                          │  REST API / Unix socket
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Docker Daemon (dockerd)                   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Images     │  │  Containers  │  │    Networks &    │  │
│  │  Management  │  │  Lifecycle   │  │    Volumes       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                          │                                   │
│                    containerd                               │
│                    (container runtime)                       │
│                          │                                   │
│                        runc                                  │
│                    (OCI runtime — actually starts container) │
└─────────────────────────────────────────────────────────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        Container 1  Container 2  Container 3
```

### Key Components

**Docker Client** — the `docker` command you type. It sends API requests to the daemon.

**Docker Daemon** (`dockerd`) — the background service that does all the work. It manages images, containers, networks, and volumes.

**containerd** — the container runtime that manages the container lifecycle (pulling images, creating containers, managing storage).

**runc** — the low-level OCI (Open Container Initiative) runtime that actually creates and starts containers using Linux kernel features.

**Docker Registry** — a storage system for images. Docker Hub is the public default. You can use private registries.

---

## 5. Images — Complete Guide

### What an Image Is

An image is an immutable, layered filesystem snapshot. It contains everything needed to run an application:
- A base operating system layer (usually a minimal Linux)
- A runtime (Python, Node.js, Java, etc.)
- Application dependencies (pip packages, npm modules, etc.)
- Application code
- Configuration and metadata

Images are identified by a **name** and a **tag**:
- `python:3.10-slim` — name is `python`, tag is `3.10-slim`
- `nginx:1.25` — name is `nginx`, tag is `1.25`
- `ubuntu:22.04` — name is `ubuntu`, tag is `22.04`
- `ubuntu` — name is `ubuntu`, tag defaults to `latest`

**Never use `latest` in production** — `latest` is just a tag that image maintainers update whenever they push a new version. If you pin to `latest`, your image changes without warning the next time you build.

### Pulling Images

```bash
# pull from Docker Hub (default registry)
docker pull python:3.10-slim
# Docker downloads each layer separately
# already-downloaded layers are reused from cache

# pull a specific digest (most reproducible — identifies exact image content)
docker pull python@sha256:abc123...

# pull from a private registry
docker pull registry.company.com/myimage:1.0

# pull all tags of an image
docker pull -a python

# check what you have locally
docker images
# or
docker image ls

# output columns:
# REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
# python       3.10-slim abc123def456   2 weeks ago    150MB
# ubuntu       22.04     def456abc789   1 month ago    77.8MB

# list with more details
docker image ls --digests    # show image digests
docker image ls --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# filter images
docker image ls python       # only python images
docker image ls --filter "dangling=true"   # untagged images (leftover from builds)
```

### Inspecting Images

```bash
# detailed JSON information about an image
docker inspect python:3.10-slim
# shows: layers, environment variables, default command,
#        exposed ports, labels, creation date, architecture

# see the layers and commands that created them
docker history python:3.10-slim
# shows each layer with size and the command that created it

# extract specific information with Go template syntax
docker inspect --format='{{.Config.Env}}' python:3.10-slim
docker inspect --format='{{.Config.Cmd}}' nginx:latest
docker inspect --format='{{.Config.ExposedPorts}}' nginx:latest

# image filesystem
docker image inspect --format='{{.RootFS.Layers}}' python:3.10-slim
# shows the SHA256 hash of each layer
```

### Managing Images

```bash
# tag an image (create an alias)
docker tag python:3.10-slim mypython:latest
docker tag myapp:1.0 myusername/myapp:1.0    # prepare for push to Docker Hub

# remove an image
docker rmi python:3.10-slim
docker image rm python:3.10-slim

# force remove (even if containers are using it)
docker rmi -f python:3.10-slim

# remove multiple images
docker rmi python:3.10-slim ubuntu:22.04

# remove all dangling images (untagged, not used by any container)
docker image prune

# remove ALL unused images (not referenced by any container)
docker image prune -a

# remove all images (WARNING: removes everything)
docker rmi $(docker images -q)

# save image to a tar file (for air-gapped environments)
docker save python:3.10-slim -o python_310_slim.tar
docker save python:3.10-slim | gzip > python_310_slim.tar.gz

# load image from tar file
docker load -i python_310_slim.tar
docker load < python_310_slim.tar.gz

# export a container's filesystem (not the image layers — flattened)
docker export my_container -o container_filesystem.tar
docker import container_filesystem.tar my_imported_image:latest
# note: export/import loses metadata like environment variables and CMD
# use save/load to preserve everything
```

### Common Base Images for ML

```bash
# ── Python images ─────────────────────────────────────────────

# python:3.10           ~900MB  full Debian with build tools
# python:3.10-slim      ~150MB  minimal Debian (recommended)
# python:3.10-alpine    ~50MB   Alpine Linux (smallest, musl libc — some packages break)
# python:3.10-bullseye          Debian Bullseye specific
# python:3.10-bookworm          Debian Bookworm (newer)

# ── Deep Learning images ──────────────────────────────────────

# tensorflow/tensorflow:2.13.0                        CPU only
# tensorflow/tensorflow:2.13.0-gpu                    GPU (CUDA)
# tensorflow/tensorflow:2.13.0-jupyter                CPU + Jupyter

# pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime       PyTorch + CUDA
# pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel         PyTorch + CUDA + build tools

# ── Jupyter images ────────────────────────────────────────────

# jupyter/base-notebook         minimal Jupyter
# jupyter/scipy-notebook        Jupyter + scipy stack (numpy, pandas, matplotlib)
# jupyter/datascience-notebook  Jupyter + R + Julia + Python science stack
# jupyter/tensorflow-notebook   Jupyter + TensorFlow
# jupyter/pytorch-notebook      Jupyter + PyTorch

# ── Database images ───────────────────────────────────────────

# postgres:15.2-alpine
# mysql:8.0
# redis:7.2-alpine
# mongo:6.0
# elasticsearch:8.9.0

# ── Web server images ─────────────────────────────────────────

# nginx:1.25-alpine
# nginx:1.25
```

---

## 6. Containers — Complete Guide

### Running Containers

```bash
# basic run
docker run nginx

# run with name
docker run --name my_nginx nginx
# without --name Docker generates a random name like "sleepy_darwin"

# run in background (detached mode)
docker run -d --name my_nginx nginx

# run and remove when it exits
docker run --rm ubuntu echo "hello"
# --rm is important for one-off tasks — avoids accumulating stopped containers

# run interactively with a terminal
docker run -it ubuntu bash
# -i = keep stdin open (interactive)
# -t = allocate a pseudo-TTY (terminal)
# you need both -i and -t for an interactive shell

# run a specific command
docker run ubuntu ls -la /
docker run python:3.10-slim python -c "import sys; print(sys.version)"
```

### Port Mapping

```bash
# map host port to container port
# -p HOST_PORT:CONTAINER_PORT
docker run -d -p 8000:8000 fastapi_app

# map to a specific host IP (only accept connections from localhost)
docker run -d -p 127.0.0.1:8000:8000 fastapi_app

# map to a random available host port (Docker chooses)
docker run -d -p 8000 fastapi_app
docker port my_container 8000    # see which host port was assigned

# map multiple ports
docker run -d -p 8000:8000 -p 5000:5000 my_app

# map a range of ports
docker run -d -p 8000-8010:8000-8010 my_app

# see port mappings for a running container
docker port my_container
```

### Container Lifecycle

```bash
# start a stopped container
docker start my_container
docker start -i my_container    # start and attach interactively

# stop a running container (sends SIGTERM, waits 10s, then SIGKILL)
docker stop my_container
docker stop --time 30 my_container   # wait 30 seconds before SIGKILL

# immediately kill a container (sends SIGKILL — no cleanup)
docker kill my_container
docker kill --signal SIGINT my_container   # send specific signal

# restart a container
docker restart my_container
docker restart --time 5 my_container  # 5 second grace period

# pause a container (freezes all processes)
docker pause my_container

# unpause
docker unpause my_container

# remove a stopped container
docker rm my_container

# force remove a running container
docker rm -f my_container

# remove all stopped containers
docker container prune

# remove all containers (running and stopped)
docker rm -f $(docker ps -aq)
```

### Inspecting Running Containers

```bash
# list running containers
docker ps
# output: CONTAINER ID, IMAGE, COMMAND, CREATED, STATUS, PORTS, NAMES

# list all containers (including stopped)
docker ps -a

# list only container IDs (useful for scripting)
docker ps -q           # running only
docker ps -aq          # all containers

# filter containers
docker ps --filter "status=exited"
docker ps --filter "name=my_app"
docker ps --filter "ancestor=python:3.10"   # containers from this image

# custom output format
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# detailed JSON information
docker inspect my_container
# shows everything: network settings, mounts, environment variables,
# restart policy, resource limits, process info

# extract specific fields
docker inspect --format='{{.State.Status}}' my_container    # running/exited/paused
docker inspect --format='{{.NetworkSettings.IPAddress}}' my_container
docker inspect --format='{{.Mounts}}' my_container

# resource usage (live, like top)
docker stats
docker stats my_container        # one specific container
docker stats --no-stream         # single snapshot, don't keep updating

# output: CPU %, MEM USAGE/LIMIT, NET I/O, BLOCK I/O, PIDS

# processes running inside a container
docker top my_container
docker top my_container aux      # with extra process details

# container filesystem changes since it started
docker diff my_container
# A = added, C = changed, D = deleted
```

### Logs

```bash
# view container logs
docker logs my_container

# follow logs in real time (like tail -f)
docker logs -f my_container

# last N lines
docker logs --tail 100 my_container
docker logs --tail 0 -f my_container   # only new logs from now

# with timestamps
docker logs -t my_container
docker logs -t --tail 50 my_container

# logs since a specific time
docker logs --since "2024-01-01T10:00:00" my_container
docker logs --since 1h my_container    # last hour
docker logs --since 30m my_container   # last 30 minutes
docker logs --until "2024-01-01T12:00:00" my_container

# filter by log level (if app writes JSON logs)
docker logs my_container 2>&1 | grep ERROR
```

### Exec — Running Commands in Running Containers

```bash
# open an interactive bash shell
docker exec -it my_container bash
docker exec -it my_container sh    # use sh if bash is not available (Alpine images)

# run a non-interactive command
docker exec my_container ls /app
docker exec my_container python -c "import pandas; print(pandas.__version__)"

# run as a specific user
docker exec -u root my_container bash
docker exec -u 1000 my_container bash

# set environment variables
docker exec -e DEBUG=true my_container python script.py

# set working directory
docker exec -w /app/data my_container ls

# copy files between host and container
docker cp local_file.txt my_container:/app/
docker cp my_container:/app/output.csv ./output.csv
docker cp my_container:/app/logs/ ./logs/    # copy entire directory
```

### Container Restart Policies

```bash
# restart policies control what happens when a container exits

# no   = never restart (default)
docker run --restart no my_app

# on-failure = restart only if exit code is non-zero
# optional: limit restart attempts
docker run --restart on-failure my_app
docker run --restart on-failure:5 my_app   # max 5 restart attempts

# always = always restart (even if manually stopped — except on docker stop)
docker run --restart always my_app

# unless-stopped = always restart UNLESS manually stopped with docker stop
# this is the most useful policy for production services
docker run --restart unless-stopped my_app

# view restart policy
docker inspect --format='{{.HostConfig.RestartPolicy}}' my_container
```

---

## 7. Dockerfile — Every Instruction Explained

A Dockerfile is a text file containing a sequence of instructions. Docker reads it top to bottom and executes each instruction to build an image. Every instruction that modifies the filesystem creates a new layer.

### FROM

```dockerfile
# FROM — specifies the base image
# MUST be the first instruction in a Dockerfile (except ARG)
# syntax: FROM image:tag [AS name]

FROM python:3.10-slim
FROM ubuntu:22.04
FROM scratch    # empty base — for building from absolute scratch (Go binaries etc.)

# with alias (for multi-stage builds)
FROM python:3.10-slim AS builder
FROM python:3.10-slim AS production

# with platform specification (for cross-platform builds)
FROM --platform=linux/amd64 python:3.10-slim
FROM --platform=linux/arm64 python:3.10-slim

# using a build argument for the base image
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim
```

### LABEL

```dockerfile
# LABEL — adds metadata to the image as key=value pairs
# purely informational — does not affect the build

LABEL maintainer="kempsly@natixis.com"
LABEL version="2.1.0"
LABEL description="Fins'AIght document intelligence pipeline"
LABEL org.opencontainers.image.source="https://github.com/kempsly/finsaight"

# view labels
# docker inspect --format='{{json .Config.Labels}}' my_image
```

### ARG

```dockerfile
# ARG — defines a build-time variable
# can be passed during docker build with --build-arg
# NOT available at runtime (use ENV for that)
# NOT persisted in the image (use ENV for that)

ARG PYTHON_VERSION=3.10          # with default value
ARG APP_VERSION                  # no default — must be passed

FROM python:${PYTHON_VERSION}-slim

ARG APP_ENV=production           # ARG after FROM is scoped to the build stage
RUN echo "Building for: $APP_ENV"

# pass during build:
# docker build --build-arg PYTHON_VERSION=3.11 --build-arg APP_ENV=dev .

# IMPORTANT: ARG values are visible in docker history
# NEVER use ARG for secrets
```

### ENV

```dockerfile
# ENV — sets environment variables in the image
# available both during build AND at runtime
# persisted in the image and in running containers

ENV PYTHONDONTWRITEBYTECODE=1     # don't create .pyc files
ENV PYTHONUNBUFFERED=1            # don't buffer stdout/stderr (important for logs)
ENV APP_HOME=/app
ENV PORT=8000

# multiple ENV in one instruction (more efficient — one layer)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    PORT=8000

# use in subsequent instructions
WORKDIR ${APP_HOME}
EXPOSE ${PORT}

# override at runtime:
# docker run -e PORT=9000 my_image
# docker run --env-file .env my_image

# view environment variables in image
# docker inspect --format='{{.Config.Env}}' my_image
```

### WORKDIR

```dockerfile
# WORKDIR — sets the working directory for subsequent instructions
# (RUN, CMD, ENTRYPOINT, COPY, ADD)
# creates the directory if it doesn't exist
# recommended over using cd in RUN commands

WORKDIR /app

# subsequent paths are relative to /app
COPY requirements.txt .    # copies to /app/requirements.txt
RUN pip install -r requirements.txt
COPY . .                   # copies to /app/

# you can use multiple WORKDIR instructions
WORKDIR /app
WORKDIR src            # now at /app/src
WORKDIR ..             # back to /app
```

### COPY

```dockerfile
# COPY — copies files from build context (your local machine) into the image
# syntax: COPY [--chown=user:group] source destination
# source = path relative to build context
# destination = absolute path OR relative to WORKDIR

COPY requirements.txt .          # copy to WORKDIR/requirements.txt
COPY requirements.txt /app/      # copy to /app/requirements.txt
COPY . .                          # copy entire build context to WORKDIR
COPY src/ /app/src/              # copy entire directory
COPY *.py /app/                  # glob patterns supported

# copy with ownership (important for non-root users)
COPY --chown=appuser:appgroup requirements.txt .

# copy from a specific build stage (multi-stage builds)
COPY --from=builder /app/dist /app/dist
COPY --from=0 /app/dist /app/dist    # by stage index

# best practice: copy requirements first, then code
# this way requirements are cached separately from your code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .    # code change here doesn't invalidate the pip cache layer
```

### ADD

```dockerfile
# ADD — like COPY but with extra features
# 1. can extract tar archives automatically
# 2. can download from URLs (not recommended — use RUN curl instead)

# extract tar archive
ADD myarchive.tar.gz /app/        # extracted into /app/

# download from URL (avoid this — use RUN wget/curl instead for better caching)
ADD https://example.com/file.txt /app/

# for simple file copying, ALWAYS prefer COPY over ADD
# ADD is harder to reason about and less predictable
# only use ADD when you specifically need tar extraction
```

### RUN

```dockerfile
# RUN — executes a command in a new layer during build
# two forms:
# shell form: RUN command args          (runs in /bin/sh -c)
# exec form:  RUN ["executable", "arg"] (no shell — more predictable)

# shell form (most common)
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

# exec form
RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

# IMPORTANT: each RUN creates a new layer
# combine related commands to minimize layers

# BAD — 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# GOOD — 1 layer, and cleans up in the same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gcc \
        libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# --no-install-recommends reduces install size
# rm -rf /var/lib/apt/lists/* removes apt cache (saves ~50MB)
# these cleanups MUST be in the same RUN as the install
# cleaning in a separate RUN doesn't reduce image size (layers are immutable)

# RUN with environment variables
RUN export PATH=$PATH:/usr/local/bin && some_command

# RUN with conditional logic
RUN if [ "$APP_ENV" = "production" ]; then \
        pip install gunicorn; \
    fi
```

### CMD

```dockerfile
# CMD — default command to run when container starts
# can be overridden by command line arguments to docker run
# only ONE CMD per Dockerfile (last one wins)
# three forms:

# exec form (RECOMMENDED — no shell, signals handled properly)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# shell form (runs in /bin/sh -c — PID 1 is sh, not your app)
CMD uvicorn main:app --host 0.0.0.0 --port 8000

# as default arguments to ENTRYPOINT
CMD ["--host", "0.0.0.0", "--port", "8000"]

# override at runtime:
# docker run my_image python other_script.py
# docker run my_image bash
```

### ENTRYPOINT

```dockerfile
# ENTRYPOINT — configures the container to run as an executable
# CANNOT be overridden by docker run arguments (only with --entrypoint flag)
# two forms:

# exec form (recommended)
ENTRYPOINT ["uvicorn", "main:app"]

# shell form
ENTRYPOINT uvicorn main:app

# ENTRYPOINT + CMD pattern:
# ENTRYPOINT defines the executable
# CMD provides default arguments that CAN be overridden

ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run my_image                    → runs: python app.py
# docker run my_image other_script.py   → runs: python other_script.py
# docker run my_image -c "print(1)"     → runs: python -c "print(1)"

# override entrypoint:
# docker run --entrypoint bash my_image

# practical example: entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### EXPOSE

```dockerfile
# EXPOSE — documents which ports the container listens on
# INFORMATIONAL ONLY — does not actually publish the port
# use -p flag with docker run to actually publish

EXPOSE 8000
EXPOSE 8000/tcp     # explicit TCP (default)
EXPOSE 5353/udp     # UDP port

# to actually make the port accessible:
# docker run -p 8000:8000 my_image

# EXPOSE is useful for:
# 1. Documentation — tells users what port to publish
# 2. docker run -P flag — publishes all EXPOSED ports to random host ports
```

### VOLUME

```dockerfile
# VOLUME — creates a mount point in the image
# marks the directory as externally mountable
# data written to this path persists even without explicit -v flag
# Docker automatically creates an anonymous volume for it

VOLUME /app/data
VOLUME /app/models
VOLUME ["/app/logs", "/app/data"]    # multiple volumes

# creates an anonymous volume (random name) if you don't specify -v
# to use a named volume instead:
# docker run -v my_data:/app/data my_image

# IMPORTANT: data in VOLUME directories is NOT included in the image
# writes to VOLUME paths during build (in RUN instructions) are not persisted
```

### USER

```dockerfile
# USER — sets the user for subsequent RUN, CMD, ENTRYPOINT instructions
# CRITICAL for security — never run your app as root

# create a non-root user and group
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

# switch to non-root user
USER appuser

# subsequent RUN, CMD, ENTRYPOINT run as this user
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# check current user inside container:
# docker exec my_container whoami

# note: file ownership matters — files must be readable by the user
RUN chown -R appuser:appgroup /app
USER appuser
```

### HEALTHCHECK

```dockerfile
# HEALTHCHECK — tells Docker how to test if the container is healthy
# Docker runs this command periodically
# container can be: starting / healthy / unhealthy

HEALTHCHECK --interval=30s \    # check every 30 seconds
            --timeout=10s \     # fail if no response in 10 seconds
            --start-period=15s \# don't check for first 15 seconds (startup time)
            --retries=3 \       # mark unhealthy after 3 consecutive failures
    CMD curl -f http://localhost:8000/health || exit 1

# for Python apps without curl
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8000/')" || exit 1

# disable health check (override inherited one)
HEALTHCHECK NONE

# check health status:
# docker inspect --format='{{.State.Health.Status}}' my_container
# docker ps (shows health status in STATUS column)
```

### ONBUILD

```dockerfile
# ONBUILD — triggers instructions when THIS image is used as a base image
# useful for creating base images for teams

# in a base image Dockerfile:
FROM python:3.10-slim
ONBUILD COPY requirements.txt /app/
ONBUILD RUN pip install -r /app/requirements.txt
ONBUILD COPY . /app/

# in a child image Dockerfile:
FROM my-company-python-base:1.0
# the ONBUILD instructions from the base image execute here
# no need to repeat COPY and RUN pip install
CMD ["python", "app.py"]
```

### STOPSIGNAL

```dockerfile
# STOPSIGNAL — sets the signal sent to the container when stopping
# default is SIGTERM

STOPSIGNAL SIGTERM    # default — graceful shutdown
STOPSIGNAL SIGINT     # Ctrl+C equivalent
STOPSIGNAL 9          # SIGKILL — immediate (no cleanup)

# important for web servers:
# uvicorn handles SIGTERM for graceful shutdown
# gunicorn handles SIGTERM
# nginx handles SIGQUIT for graceful shutdown
```

### SHELL

```dockerfile
# SHELL — overrides the default shell used for shell form RUN, CMD, ENTRYPOINT
# default on Linux: ["/bin/sh", "-c"]
# default on Windows: ["cmd", "/S", "/C"]

SHELL ["/bin/bash", "-c"]    # use bash instead of sh
# now you can use bash-specific syntax in RUN

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# -o pipefail: makes pipes fail if any command in the pipe fails
# important for: RUN curl ... | tar ... — fails if curl fails
```

---

## 8. Building Images — All Options

```bash
# basic build
docker build -t myimage:1.0 .
# -t = tag (name:version)
# .  = build context (directory containing Dockerfile)

# specify Dockerfile path
docker build -f path/to/Dockerfile -t myimage:1.0 .
docker build -f Dockerfile.production -t myimage:prod .

# build context can be a URL
docker build https://github.com/kempsly/finsaight.git

# build without cache (force rebuild all layers)
docker build --no-cache -t myimage:1.0 .

# pass build arguments
docker build --build-arg PYTHON_VERSION=3.11 -t myimage:1.0 .
docker build --build-arg APP_ENV=production --build-arg VERSION=2.0 .

# target a specific stage in multi-stage build
docker build --target builder -t myimage:builder .
docker build --target production -t myimage:prod .

# build for multiple platforms (cross-platform)
docker buildx build --platform linux/amd64,linux/arm64 -t myimage:1.0 .

# set resource limits during build
docker build --memory 4g --cpu-quota 100000 -t myimage:1.0 .

# show build output with progress
docker build --progress=plain -t myimage:1.0 .    # verbose
docker build --progress=tty -t myimage:1.0 .      # default

# build and push in one command
docker buildx build --push -t myusername/myimage:1.0 .

# add labels during build (override Dockerfile LABEL)
docker build --label "version=1.0" --label "env=prod" -t myimage:1.0 .

# squash all layers into one (experimental)
docker build --squash -t myimage:1.0 .
```

### The Build Cache

Understanding the build cache is the most important optimization for fast builds.

```dockerfile
# Docker checks each instruction against its cache
# A cache miss invalidates ALL subsequent layers

# cache is invalidated when:
# 1. The instruction itself changes
# 2. For COPY/ADD: the files being copied change
# 3. A previous layer was invalidated

# OPTIMAL ORDER (most stable to most frequently changing):
FROM python:3.10-slim                    # layer 1: almost never changes
ENV PYTHONDONTWRITEBYTECODE=1 \          # layer 2: rarely changes
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install    # layer 3: rarely changes
COPY requirements.txt .                  # layer 4: changes when dependencies change
RUN pip install -r requirements.txt      # layer 5: only rebuilt when layer 4 changes
COPY . .                                 # layer 6: changes often (your code)
CMD [...]                                # layer 7: rarely changes
```

---

## 9. Volumes — Complete Guide

### Why Volumes Are Needed

Containers are ephemeral. When a container stops or is removed, all data written to its filesystem is lost. If your ML model saves trained weights to `/app/models` inside the container, those weights disappear when the container is removed.

Volumes solve this by storing data outside the container's lifecycle.

### Three Types of Storage

**Named Volumes** — managed by Docker, stored in Docker's storage area (`/var/lib/docker/volumes/`). Best for persisting application data.

**Bind Mounts** — map a specific path on your host machine to a path in the container. Best for development (live code reloading).

**tmpfs Mounts** — stored in the host's memory only. Never written to disk. Best for sensitive temporary data.

### Named Volumes

```bash
# create a named volume
docker volume create ml_models
docker volume create --driver local ml_models    # explicitly use local driver

# create with options (local driver)
docker volume create \
    --driver local \
    --opt type=none \
    --opt device=/home/kempsly/data \
    --opt o=bind \
    my_data

# list all volumes
docker volume ls

# filter volumes
docker volume ls --filter "name=ml"
docker volume ls --filter "dangling=true"    # volumes not used by any container

# inspect a volume
docker volume inspect ml_models
# shows: mount point on host, driver, scope, creation date

# use volume in a container
docker run -v ml_models:/app/models my_app
docker run --mount type=volume,source=ml_models,target=/app/models my_app

# remove a volume
docker volume rm ml_models

# remove all unused volumes
docker volume prune

# backup a volume
docker run --rm \
    -v ml_models:/source:ro \
    -v $(pwd):/backup \
    ubuntu tar czf /backup/ml_models_backup.tar.gz -C /source .

# restore a volume from backup
docker run --rm \
    -v ml_models:/target \
    -v $(pwd):/backup:ro \
    ubuntu tar xzf /backup/ml_models_backup.tar.gz -C /target
```

### Bind Mounts

```bash
# map host directory to container
# -v /absolute/host/path:/container/path
docker run -v /Users/kempsly/projects/finsaight:/app my_app

# use $(pwd) for current directory
docker run -v $(pwd):/app my_app

# read-only bind mount
docker run -v $(pwd)/data:/app/data:ro my_app
# :ro prevents the container from modifying files on the host

# useful patterns for development
docker run \
    -v $(pwd):/app \            # live code reloading
    -v $(pwd)/data:/app/data:ro \   # read-only data
    -p 8000:8000 \
    my_app uvicorn main:app --reload   # uvicorn --reload watches for changes

# --mount syntax (more explicit, recommended in scripts)
docker run \
    --mount type=bind,source=$(pwd),target=/app \
    --mount type=bind,source=$(pwd)/data,target=/app/data,readonly \
    my_app
```

### tmpfs Mounts

```bash
# tmpfs — stored in memory only, never on disk
# useful for: sensitive data (tokens, passwords), temporary files
# data is lost when container stops

docker run --tmpfs /tmp my_app
docker run --tmpfs /tmp:rw,size=100m my_app    # 100MB limit
docker run --mount type=tmpfs,destination=/tmp,tmpfs-size=100m my_app
```

### Volume Sharing Between Containers

```bash
# share a volume between multiple containers
docker run -d --name trainer -v ml_models:/app/models my_trainer python train.py
docker run -d --name server  -v ml_models:/app/models:ro -p 8000:8000 my_server

# data container pattern (older pattern, less common now)
docker create --name data_container -v /app/data ubuntu
docker run --volumes-from data_container my_app
```

---

## 10. Networks — Complete Guide

### Network Types

Docker has several built-in network drivers:

**bridge** — the default. Creates a private internal network on the host. Containers on the same bridge network can communicate. Containers are isolated from the host and from other bridge networks. Best for most use cases.

**host** — the container shares the host's network stack. No isolation — the container's ports are directly the host's ports. Useful for performance-critical applications. Linux only (doesn't work on Mac/Windows Docker Desktop).

**none** — completely disables networking. The container has no network interfaces. Useful for security-sensitive workloads that need no network access.

**overlay** — used for Docker Swarm (multi-host networking). Spans multiple Docker hosts. Not covered here.

**macvlan** — assigns a MAC address to the container, making it appear as a physical device on the network. Advanced use case.

### Default Bridge Network

```bash
# when you run a container without specifying a network
# it connects to the default bridge network (docker0)

docker run -d --name container1 ubuntu sleep 3600
docker run -d --name container2 ubuntu sleep 3600

# containers on default bridge CAN communicate by IP
docker inspect container1 | grep IPAddress    # e.g. 172.17.0.2
# from container2: ping 172.17.0.2 works

# BUT: containers on default bridge CANNOT communicate by name
# from container2: ping container1 FAILS (no DNS resolution)
# this is why you should ALWAYS create custom bridge networks
```

### Custom Bridge Networks

```bash
# create a custom bridge network
docker network create finsaight_net

# create with custom subnet and gateway
docker network create \
    --driver bridge \
    --subnet 172.20.0.0/16 \
    --gateway 172.20.0.1 \
    --ip-range 172.20.1.0/24 \
    finsaight_net

# run containers on the custom network
docker run -d --name api --network finsaight_net my_api
docker run -d --name db  --network finsaight_net postgres:15

# containers on custom networks CAN communicate by name (DNS resolution built-in)
# from the api container: ping db → resolves to db's IP automatically

# connect an already-running container to a network
docker network connect finsaight_net my_container

# disconnect from a network
docker network disconnect finsaight_net my_container

# list networks
docker network ls

# inspect a network
docker network inspect finsaight_net
# shows: containers connected, subnet, gateway, driver, options

# remove a network
docker network rm finsaight_net

# remove all unused networks
docker network prune
```

### Network Aliases

```bash
# give a container an alias on a network
docker run -d \
    --name primary_db \
    --network finsaight_net \
    --network-alias database \
    postgres:15

# another container can now reach it as either "primary_db" or "database"
# from api container: psql -h database -U user finsaight
# useful for blue-green deployments — swap the container behind the alias
```

### DNS in Docker Networks

```bash
# Docker runs an embedded DNS server for custom networks
# DNS server is at 127.0.0.11 inside containers

# service discovery works by container name
# if container is named "db", it's reachable as "db"
# if service is named "database" in compose, it's reachable as "database"

# multiple containers with same alias = round-robin DNS (basic load balancing)
docker run -d --name api1 --network mynet --network-alias api my_api
docker run -d --name api2 --network mynet --network-alias api my_api
docker run -d --name api3 --network mynet --network-alias api my_api
# requests to "api" round-robin between api1, api2, api3
```

---

## 11. Environment Variables & Secrets

### Methods of Passing Environment Variables

```bash
# ── Method 1 — inline with -e flag ────────────────────────────
docker run -e PORT=8000 -e DEBUG=false my_app
docker run -e GROQ_API_KEY=sk-abc123 my_app

# ── Method 2 — inherit from host shell ────────────────────────
export GROQ_API_KEY=sk-abc123
docker run -e GROQ_API_KEY my_app   # no = means inherit from host

# ── Method 3 — .env file ──────────────────────────────────────
# .env file format:
# KEY=value
# ANOTHER_KEY=another_value
docker run --env-file .env my_app

# ── Method 4 — Docker secrets (production) ────────────────────
# Docker secrets are stored encrypted and only available to services
# that explicitly request them (Swarm mode)
echo "my_secret_password" | docker secret create db_password -
docker service create \
    --secret db_password \
    --env DB_PASSWORD_FILE=/run/secrets/db_password \
    my_app
# inside container: /run/secrets/db_password contains the secret
```

### Accessing Environment Variables in Python

```python
import os
from dotenv import load_dotenv

# load .env file for local development
load_dotenv()

# access variables
api_key   = os.getenv("GROQ_API_KEY")
debug     = os.getenv("DEBUG", "false").lower() == "true"
port      = int(os.getenv("PORT", "8000"))
db_url    = os.environ["DATABASE_URL"]    # raises KeyError if missing

# validate required variables at startup
required = ["GROQ_API_KEY", "DATABASE_URL", "SECRET_KEY"]
missing  = [var for var in required if not os.getenv(var)]
if missing:
    raise ValueError(f"Missing required environment variables: {missing}")
```

### Security Rules

```bash
# NEVER put secrets in Dockerfile
# they end up in image history and anyone with the image can see them
docker history my_image    # shows all ENV values

# NEVER commit .env to git
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore

# NEVER print secrets in logs
# bad:
print(f"Connecting with key: {api_key}")
# good:
print(f"Connecting with key: {api_key[:8]}...")

# use different .env files per environment
# .env.development  ← your local keys
# .env.staging      ← staging keys
# .env.production   ← production keys (never committed)
```

---

## 12. Resource Management

### CPU Limits

```bash
# limit CPU usage
# --cpus = number of CPUs the container can use (can be decimal)
docker run --cpus="2.0" my_app    # max 2 CPU cores
docker run --cpus="0.5" my_app    # max 50% of 1 CPU core

# --cpu-shares = relative weight (default 1024)
# only applies when CPUs are under contention
docker run --cpu-shares=512 my_app     # half the default priority
docker run --cpu-shares=2048 my_app    # double the default priority

# pin to specific CPUs
docker run --cpuset-cpus="0,1" my_app     # only use CPUs 0 and 1
docker run --cpuset-cpus="0-3" my_app     # CPUs 0, 1, 2, 3
```

### Memory Limits

```bash
# limit memory
docker run --memory="2g" my_app         # max 2 GB RAM
docker run --memory="512m" my_app       # max 512 MB RAM
docker run -m 4g my_app                 # short form

# swap memory (memory + swap combined)
docker run --memory="1g" --memory-swap="2g" my_app
# --memory-swap = total (memory + swap), not just swap
# swap = memory-swap - memory = 2g - 1g = 1g of swap

# disable swap entirely
docker run --memory="1g" --memory-swap="1g" my_app

# memory reservation (soft limit — Docker tries to keep below this)
docker run --memory-reservation="512m" my_app

# behavior when OOM (Out of Memory)
docker run --oom-kill-disable my_app    # don't kill container on OOM (risky)
docker run --oom-score-adj=-500 my_app  # lower OOM priority (-1000 to 1000)
```

### Storage Limits

```bash
# limit container's writable layer size
docker run --storage-opt size=10G my_app
# requires overlay2 storage driver with xfs backing filesystem
```

---

## 13. Logging

### Log Drivers

Docker supports multiple log drivers — they control where container logs are stored.

```bash
# check default log driver
docker info | grep "Logging Driver"

# available log drivers:
# json-file  = default, stores JSON files on host (docker logs works)
# syslog     = sends to system syslog
# journald   = sends to systemd journal
# gelf       = sends to Graylog
# fluentd    = sends to Fluentd
# awslogs    = sends to AWS CloudWatch
# splunk     = sends to Splunk
# none       = disables logging

# set log driver for a container
docker run --log-driver json-file my_app
docker run --log-driver none my_app      # disable logging

# configure log driver options
docker run \
    --log-driver json-file \
    --log-opt max-size=100m \    # max size before rotation
    --log-opt max-file=5 \       # keep 5 rotated files
    my_app

docker run \
    --log-driver awslogs \
    --log-opt awslogs-region=eu-west-1 \
    --log-opt awslogs-group=/ecs/finsaight \
    --log-opt awslogs-stream=api \
    my_app

# set default log driver for all containers (in /etc/docker/daemon.json)
# {
#   "log-driver": "json-file",
#   "log-opts": {
#     "max-size": "100m",
#     "max-file": "5"
#   }
# }
```

### Reading Logs

```bash
docker logs my_container                    # all logs
docker logs -f my_container                 # follow (stream) logs
docker logs --tail 100 my_container         # last 100 lines
docker logs -t my_container                 # with timestamps
docker logs --since 1h my_container         # last hour
docker logs --since "2024-01-01" my_container
docker logs --until "2024-01-02" my_container
docker logs --since 30m --until 10m my_container   # 30 to 10 minutes ago

# pipe to grep
docker logs my_container 2>&1 | grep ERROR
docker logs my_container 2>&1 | grep -i "exception" | tail -20

# redirect logs to file
docker logs my_container > app.log 2>&1
```

---

## 14. Health Checks

### What Health Checks Do

Without a health check, Docker considers a container "healthy" as soon as the process starts. But your application might take 10 seconds to initialize, or it might crash after startup, or it might be running but unable to handle requests.

A health check is a command Docker runs periodically inside the container. Based on the exit code (0 = healthy, 1 = unhealthy), Docker updates the container's health status.

Other tools (Docker Compose depends_on, Kubernetes, load balancers) can use this health status to route traffic only to healthy containers.

```dockerfile
# in Dockerfile

# using curl (need to install it)
HEALTHCHECK --interval=30s \
            --timeout=10s \
            --start-period=20s \
            --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# using wget (usually available in slim images)
HEALTHCHECK CMD wget -q -O /dev/null http://localhost:8000/ || exit 1

# using Python
HEALTHCHECK CMD python -c "\
import urllib.request; \
urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# check database connection
HEALTHCHECK CMD pg_isready -U $POSTGRES_USER || exit 1

# disable inherited health check
HEALTHCHECK NONE
```

```bash
# add health check at runtime (overrides Dockerfile HEALTHCHECK)
docker run \
    --health-cmd="curl -f http://localhost:8000/ || exit 1" \
    --health-interval=30s \
    --health-timeout=10s \
    --health-start-period=20s \
    --health-retries=3 \
    my_app

# check health status
docker inspect --format='{{.State.Health.Status}}' my_container
# possible values: starting, healthy, unhealthy

docker inspect --format='{{json .State.Health}}' my_container
# shows full health check history with output and exit codes

# health in docker ps
docker ps
# STATUS column shows: Up 5 minutes (healthy) or Up 5 minutes (unhealthy)
```

---

## 15. Multi-Stage Builds

Multi-stage builds allow you to use multiple FROM instructions in a single Dockerfile. Each FROM starts a new build stage. You can selectively copy artifacts from one stage to another, leaving behind everything you don't need in the final image.

### Why Multi-Stage Builds Matter

A Python application typically needs build tools (gcc, g++, cmake) to compile certain packages (numpy, pandas, psycopg2). But once compiled, the build tools are not needed at runtime. Without multi-stage builds, those tools end up in your production image, making it hundreds of megabytes larger than necessary.

```dockerfile
# Dockerfile.multistage

# ════════════════════════════════════════════
# STAGE 1: BUILDER
# Full Python image with build tools
# We install and compile all packages here
# ════════════════════════════════════════════
FROM python:3.10 AS builder

WORKDIR /app

# install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        cmake \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install Python packages
# --user installs to ~/.local instead of system Python
# this makes it easy to copy to the next stage
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ════════════════════════════════════════════
# STAGE 2: PRODUCTION
# Slim image without build tools
# Only copy what's needed to run the app
# ════════════════════════════════════════════
FROM python:3.10-slim AS production

WORKDIR /app

# install only RUNTIME system dependencies (not build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \        # runtime PostgreSQL client library
        curl \          # for health checks
    && rm -rf /var/lib/apt/lists/*

# copy installed Python packages from builder stage
# NOT the compiler or build tools — just the compiled packages
COPY --from=builder /root/.local /root/.local

# copy application code
COPY . .

# create non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser && \
    chown -R appuser:appgroup /app

USER appuser

# make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
# build only the production stage
docker build --target production -t my_app:prod .

# build only the builder stage (useful for debugging)
docker build --target builder -t my_app:builder .

# compare sizes
docker images | grep my_app
# my_app:builder    ~900MB
# my_app:prod       ~200MB
```

### Multi-Stage for ML

```dockerfile
# Dockerfile for ML model training + serving

# ════════════════════════════════════════════
# STAGE 1: TRAINING ENVIRONMENT
# Full environment for training
# ════════════════════════════════════════════
FROM python:3.10 AS trainer

WORKDIR /app
COPY requirements_train.txt .
RUN pip install --no-cache-dir -r requirements_train.txt
# includes: xgboost, sklearn, optuna, shap, mlflow, jupyter

COPY train/ ./train/
COPY data/ ./data/

CMD ["python", "train/train.py"]


# ════════════════════════════════════════════
# STAGE 2: SERVING ENVIRONMENT
# Minimal environment for inference only
# ════════════════════════════════════════════
FROM python:3.10-slim AS server

WORKDIR /app
COPY requirements_serve.txt .
RUN pip install --no-cache-dir -r requirements_serve.txt
# includes: fastapi, uvicorn, xgboost — NOT optuna, shap, mlflow

# copy only the serving code, not training code
COPY api/ ./api/

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 16. Docker Registry

### Docker Hub

```bash
# create account at hub.docker.com

# login
docker login
# prompts for username and password
# credentials stored in ~/.docker/config.json

# login to specific registry
docker login registry.company.com
docker login ghcr.io    # GitHub Container Registry

# logout
docker logout

# tag image for Docker Hub
# format: username/repository:tag
docker tag myapp:1.0 kempsly/finsaight:1.0
docker tag myapp:1.0 kempsly/finsaight:latest

# push image
docker push kempsly/finsaight:1.0
docker push kempsly/finsaight:latest

# pull image
docker pull kempsly/finsaight:1.0

# search Docker Hub
docker search python --limit 10
docker search --filter "is-official=true" python
docker search --filter "stars=100" python
```

### Private Registries

```bash
# AWS Elastic Container Registry (ECR)
aws ecr get-login-password --region eu-west-1 | \
    docker login --username AWS --password-stdin \
    123456789.dkr.ecr.eu-west-1.amazonaws.com

docker tag myapp:1.0 123456789.dkr.ecr.eu-west-1.amazonaws.com/finsaight:1.0
docker push 123456789.dkr.ecr.eu-west-1.amazonaws.com/finsaight:1.0

# GitHub Container Registry (ghcr.io)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker tag myapp:1.0 ghcr.io/kempsly/finsaight:1.0
docker push ghcr.io/kempsly/finsaight:1.0

# run your own private registry
docker run -d \
    --name registry \
    -p 5000:5000 \
    -v registry_data:/var/lib/registry \
    registry:2

docker tag myapp:1.0 localhost:5000/myapp:1.0
docker push localhost:5000/myapp:1.0
docker pull localhost:5000/myapp:1.0
```

---

## 17. Security Best Practices

```dockerfile
# ── 1. Never run as root ──────────────────────────────────────
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser && \
    chown -R appuser:appgroup /app
USER appuser

# ── 2. Use specific image versions ────────────────────────────
FROM python:3.10.13-slim    # exact version, not "3.10-slim"
# latest, 3.10, 3.10-slim all update over time

# ── 3. Minimize installed packages ────────────────────────────
RUN apt-get install -y --no-install-recommends \
    only-what-you-need
# --no-install-recommends avoids pulling in suggested packages

# ── 4. Keep secrets out of images ─────────────────────────────
# use --env-file at runtime, not ENV in Dockerfile

# ── 5. Scan images for vulnerabilities ────────────────────────
docker scout cves myimage:1.0           # Docker Scout (built-in)
docker scan myimage:1.0                 # older docker scan command

# ── 6. Use .dockerignore ──────────────────────────────────────
# prevents secrets and large files from entering build context

# ── 7. Drop capabilities ──────────────────────────────────────
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE my_app

# ── 8. Read-only filesystem ───────────────────────────────────
docker run --read-only --tmpfs /tmp my_app
# container can only write to explicitly allowed paths

# ── 9. No privilege escalation ───────────────────────────────
docker run --security-opt no-new-privileges my_app

# ── 10. Network isolation ─────────────────────────────────────
docker run --network none my_app    # no network if not needed
```

---

## 18. Debugging & Troubleshooting

```bash
# ── Container won't start ─────────────────────────────────────
docker logs my_container              # check for error messages
docker inspect my_container          # check configuration
docker run -it --entrypoint bash my_image   # override entrypoint to debug

# ── Container crashes immediately ────────────────────────────
docker run --rm my_image             # run and see output before removal
docker ps -a                         # see exit code in STATUS column
docker inspect --format='{{.State.ExitCode}}' my_container

# ── Container is unhealthy ────────────────────────────────────
docker inspect --format='{{json .State.Health}}' my_container
# shows last 5 health check results with output

# ── Can't connect to container port ──────────────────────────
docker ps                            # verify port mapping
docker inspect --format='{{json .NetworkSettings.Ports}}' my_container
docker exec my_container ss -tlnp    # check what's listening inside

# ── High CPU or memory ────────────────────────────────────────
docker stats my_container            # live resource usage
docker top my_container              # processes inside

# ── Network issues ────────────────────────────────────────────
docker exec my_container ping other_container
docker exec my_container curl http://other_service:8000/
docker network inspect my_network    # check which containers are connected

# ── Image build fails ─────────────────────────────────────────
docker build --no-cache --progress=plain .   # verbose output, no cache
# add intermediate debugging steps:
RUN ls -la /app                     # see what's in the directory
RUN pip list                        # see what's installed
RUN env                             # see environment variables

# ── Disk space issues ─────────────────────────────────────────
docker system df                    # show disk usage by category
docker system prune -a              # remove everything unused
docker image prune -a               # only remove unused images
docker container prune              # only remove stopped containers
docker volume prune                 # only remove unused volumes

# ── Interactive debugging ─────────────────────────────────────
# exec into running container
docker exec -it my_container bash

# run image with shell (bypass CMD)
docker run -it --rm --entrypoint bash my_image

# run with host network (debug network issues)
docker run -it --network host my_image bash
```

---

---

# PART 2 — DOCKER COMPOSE

---

## 19. What is Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. Instead of managing each container with separate `docker run` commands — which gets unwieldy quickly — you define your entire application stack in a single YAML file called `docker-compose.yml`.

With one command (`docker compose up`), Docker Compose:
1. Reads your `docker-compose.yml`
2. Creates a dedicated network for your application
3. Pulls or builds all required images
4. Creates and starts all containers in the right order
5. Sets up all volumes and network connections

### Compose File Versions

The Compose file format has evolved through several versions:

- **Version 2.x** — added services, volumes, networks
- **Version 3.x** — added deploy (for Swarm), health checks, configs, secrets
- **Latest (no version field)** — current format, recommended for new projects

```yaml
# modern Compose files don't need a version field
# just start with services:

services:
  api:
    image: nginx
```

---

## 20. docker-compose.yml — Every Field Explained

```yaml
# docker-compose.yml — complete reference

# ── Top-level keys ────────────────────────────────────────────
# services:  (required) defines the containers
# networks:  (optional) defines custom networks
# volumes:   (optional) defines named volumes
# configs:   (optional) defines configuration objects (Swarm)
# secrets:   (optional) defines secrets (Swarm)

services:

  # ── Service definition ────────────────────────────────────────
  myservice:

    # ── Image or build ────────────────────────────────────────────
    # Option A: use an existing image
    image: python:3.10-slim

    # Option B: build from Dockerfile
    build:
      context: .                    # build context directory
      dockerfile: Dockerfile        # Dockerfile name (default: Dockerfile)
      args:                         # build arguments (like --build-arg)
        PYTHON_VERSION: "3.10"
        APP_ENV: production
      target: production            # multi-stage build target
      cache_from:                   # use these images as cache sources
        - python:3.10-slim
      labels:                       # add labels to the built image
        version: "1.0"
      shm_size: "128m"              # shared memory size for build

    # ── Container naming ──────────────────────────────────────────
    container_name: finsaight_api   # explicit container name
    # without this: projectname_servicename_1

    # ── Ports ─────────────────────────────────────────────────────
    ports:
      - "8000:8000"                 # HOST:CONTAINER
      - "8000"                      # random host port : 8000
      - "127.0.0.1:8000:8000"       # bind to localhost only
      - target: 8000                # long form
        published: "8000"
        protocol: tcp
        mode: host

    # ── Environment ───────────────────────────────────────────────
    environment:
      DEBUG: "false"
      PORT: "8000"
      API_KEY: ${API_KEY}           # from host environment or .env file
      DATABASE_URL: postgresql://db:5432/mydb   # reference other service by name

    env_file:
      - .env                        # load all variables from .env file
      - .env.production             # load additional file

    # ── Volumes ───────────────────────────────────────────────────
    volumes:
      - ml_models:/app/models       # named volume
      - ./logs:/app/logs            # bind mount (relative path)
      - /absolute/path:/app/data    # bind mount (absolute path)
      - ./config.yml:/app/config.yml:ro   # read-only bind mount
      - type: volume                # long form
        source: ml_models
        target: /app/models
        read_only: false
      - type: bind
        source: ./logs
        target: /app/logs

    # ── Networks ──────────────────────────────────────────────────
    networks:
      - frontend_net
      - backend_net
      # or with aliases:
      # frontend_net:
      #   aliases:
      #     - api
      #     - web

    # ── Dependencies ──────────────────────────────────────────────
    depends_on:
      - db                          # simple: just wait for container to start
      db:                           # condition-based (recommended)
        condition: service_healthy  # wait for health check to pass
      redis:
        condition: service_started  # just wait for container to start
      migrations:
        condition: service_completed_successfully   # wait for one-off task to complete

    # ── Command and Entrypoint ────────────────────────────────────
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    # overrides CMD from Dockerfile
    # can also be a list:
    # command: ["uvicorn", "main:app", "--host", "0.0.0.0"]

    entrypoint: /docker-entrypoint.sh
    # overrides ENTRYPOINT from Dockerfile

    # ── Restart policy ────────────────────────────────────────────
    restart: unless-stopped
    # no | always | on-failure | on-failure:3 | unless-stopped

    # ── Health check ──────────────────────────────────────────────
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
      # disable inherited health check:
      # test: ["NONE"]

    # ── Resource limits ───────────────────────────────────────────
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G
        reservations:
          cpus: "0.5"
          memory: 1G

    # ── Logging ───────────────────────────────────────────────────
    logging:
      driver: json-file
      options:
        max-size: "100m"
        max-file: "5"

    # ── Labels ────────────────────────────────────────────────────
    labels:
      - "com.example.version=1.0"
      - "com.example.environment=production"

    # ── User ──────────────────────────────────────────────────────
    user: "1001:1001"               # run as specific uid:gid

    # ── Working directory ─────────────────────────────────────────
    working_dir: /app

    # ── Hostname ──────────────────────────────────────────────────
    hostname: finsaight-api

    # ── Extra hosts ───────────────────────────────────────────────
    extra_hosts:
      - "host.docker.internal:host-gateway"   # access host machine from container

    # ── Stdin and TTY ─────────────────────────────────────────────
    stdin_open: true    # -i flag
    tty: true           # -t flag
    # needed for interactive containers (e.g. Jupyter)

    # ── Privileged mode (avoid if possible) ──────────────────────
    privileged: false   # gives container full host access (security risk)

    # ── Security options ──────────────────────────────────────────
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE

    # ── Sysctls ───────────────────────────────────────────────────
    sysctls:
      net.core.somaxconn: "1024"

    # ── Ulimits ───────────────────────────────────────────────────
    ulimits:
      nofile:
        soft: 65536
        hard: 65536

    # ── Stop signal and timeout ───────────────────────────────────
    stop_signal: SIGTERM
    stop_grace_period: 30s      # wait this long for graceful shutdown

    # ── Profiles ──────────────────────────────────────────────────
    profiles:
      - production              # only start when --profile production is used

    # ── Init process ──────────────────────────────────────────────
    init: true
    # runs a tiny init process as PID 1
    # properly handles signals and zombie processes
    # recommended for production

    # ── Platform ──────────────────────────────────────────────────
    platform: linux/amd64       # force specific platform

# ── Top-level volumes ─────────────────────────────────────────
volumes:
  ml_models:                    # basic named volume
  postgres_data:
    driver: local               # explicitly local driver
  s3_data:
    driver: rclone              # third-party driver
    driver_opts:
      type: s3
      path: mybucket/data
  external_volume:
    external: true              # use pre-existing volume (not created by compose)
    name: my_existing_volume

# ── Top-level networks ────────────────────────────────────────
networks:
  frontend_net:                 # basic network
  backend_net:
    driver: bridge
    ipam:                       # IP Address Management
      driver: default
      config:
        - subnet: "172.20.0.0/16"
          gateway: "172.20.0.1"
  external_net:
    external: true              # use pre-existing network
    name: my_existing_network
```

---

## 21. Services — Complete Guide

### Service Build Configuration

```yaml
services:
  api:
    build:
      context: ./api              # directory containing Dockerfile
      dockerfile: Dockerfile.prod # custom Dockerfile name
      args:
        - PYTHON_VERSION=3.10
        - BUILD_DATE=${BUILD_DATE}
      target: production           # stage name in multi-stage build
      cache_from:
        - myregistry/myapp:cache
      labels:
        - "built-by=docker-compose"
      platforms:
        - linux/amd64
        - linux/arm64
      ssh:
        - default                  # pass SSH agent for private git repos
```

### Image Pull Policy

```yaml
services:
  api:
    image: python:3.10-slim
    pull_policy: always       # always pull from registry
    # never    = never pull, use local only
    # always   = always pull latest from registry
    # missing  = pull only if not available locally (default)
    # build    = always build from Dockerfile
```

### Service Replicas

```yaml
services:
  api:
    image: my_api
    deploy:
      replicas: 3             # run 3 instances of this service
      update_config:
        parallelism: 1        # update 1 replica at a time
        delay: 10s            # wait 10s between updates
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

---

## 22. Networking in Compose

### Default Network

When you run `docker compose up`, Docker Compose automatically creates a default bridge network named `projectname_default`. All services are connected to this network and can reach each other by service name.

```yaml
# NO explicit networks needed for basic service-to-service communication
services:
  api:
    build: .
    # api can reach "db" at http://db:5432

  db:
    image: postgres:15
    # db can reach "api" at http://api:8000
```

### Custom Networks

```yaml
services:
  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend    # only on backend, not accessible from frontend

  nginx:
    networks:
      - frontend   # only on frontend, proxies to api

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true    # no external access — only containers can reach it
```

### Network Aliases

```yaml
services:
  api:
    networks:
      backend:
        aliases:
          - application
          - web-api
    # other containers can reach this service as:
    # "api", "application", or "web-api"
```

### Static IPs

```yaml
services:
  api:
    networks:
      backend:
        ipv4_address: 172.20.0.10   # assign static IP

networks:
  backend:
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

---

## 23. Volumes in Compose

```yaml
services:
  api:
    volumes:
      # named volume — persists between container restarts
      - ml_models:/app/models

      # bind mount — maps host path to container path
      - ./app:/app                      # relative path (relative to compose file)
      - /absolute/host/path:/app/data   # absolute path

      # read-only bind mount
      - ./config:/app/config:ro

      # tmpfs — memory only, never written to disk
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100m

      # long form with all options
      - type: volume
        source: ml_models
        target: /app/models
        volume:
          nocopy: true    # don't copy container data to volume on creation

  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  ml_models:
  postgres_data:

  # external volume — must exist before compose up
  shared_data:
    external: true
    name: company_shared_data

  # volume with custom driver
  nfs_data:
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw
      device: ":/path/to/dir"
```

---

## 24. Environment & Config in Compose

### Variable Substitution

```yaml
# docker-compose.yml automatically reads .env from the same directory
# variables can be used with ${VARIABLE} syntax

services:
  api:
    image: myapp:${APP_VERSION:-1.0}   # ${VAR:-default} syntax
    environment:
      PORT: ${PORT:-8000}              # use 8000 if PORT not set
      DEBUG: ${DEBUG:?DEBUG must be set}  # error if not set
```

### Multiple Compose Files

```bash
# override with docker-compose.override.yml (automatically merged)
# docker-compose.yml (base)
# docker-compose.override.yml (automatically applied)

# explicitly specify files
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

```yaml
# docker-compose.yml (base)
services:
  api:
    build: .
    environment:
      DEBUG: "false"

# docker-compose.override.yml (development overrides, auto-applied)
services:
  api:
    command: uvicorn main:app --reload
    environment:
      DEBUG: "true"
    volumes:
      - .:/app    # live code reloading in development

# docker-compose.prod.yml (production overrides, explicit)
services:
  api:
    image: registry/myapp:${VERSION}
    restart: unless-stopped
    deploy:
      replicas: 3
```

### Configs (Swarm only)

```yaml
services:
  api:
    configs:
      - source: nginx_conf
        target: /etc/nginx/nginx.conf
        mode: 0440

configs:
  nginx_conf:
    file: ./nginx.conf
```

---

## 25. Depends On & Health Checks in Compose

### The Problem with Simple depends_on

```yaml
# PROBLEM — simple depends_on only waits for container to START
# it does NOT wait for the service to be READY
services:
  api:
    depends_on:
      - db       # waits for db container to start, NOT for postgres to be ready
  db:
    image: postgres:15
```

PostgreSQL takes a few seconds to initialize. If the API starts immediately after the container starts, its database connection will fail.

### Solution — Condition-Based depends_on

```yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy    # wait for health check to pass
      redis:
        condition: service_started    # just wait for start
      migrations:
        condition: service_completed_successfully   # wait for it to finish

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb

  redis:
    image: redis:7.2-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

  migrations:
    build: .
    command: python manage.py migrate
    depends_on:
      db:
        condition: service_healthy
    restart: "no"    # don't restart — it's a one-off task
```

---

## 26. Profiles — Conditional Services

Profiles let you define services that only start under certain conditions.

```yaml
services:
  # always started (no profile)
  api:
    build: .
    ports:
      - "8000:8000"

  db:
    image: postgres:15

  # only started with --profile tools
  pgadmin:
    image: dpage/pgadmin4
    profiles:
      - tools
    ports:
      - "5050:80"

  # only started with --profile training
  trainer:
    build: .
    command: python train.py
    profiles:
      - training
    volumes:
      - ml_models:/app/models

  # only started with --profile monitoring
  prometheus:
    image: prom/prometheus
    profiles:
      - monitoring

  grafana:
    image: grafana/grafana
    profiles:
      - monitoring
```

```bash
# start base services only
docker compose up -d

# start with tools profile (includes pgadmin)
docker compose --profile tools up -d

# start with multiple profiles
docker compose --profile tools --profile monitoring up -d

# run training (one-off)
docker compose --profile training run trainer
```

---

## 27. Scaling Services

```bash
# scale a service to multiple instances
docker compose up --scale api=3

# scale multiple services
docker compose up --scale api=3 --scale worker=5

# WARNING: scaling doesn't work with container_name
# remove container_name when using scaling

# scaling with load balancing
# use nginx or a load balancer to distribute requests across instances
```

```yaml
# docker-compose.yml for scalable services
services:
  api:
    build: .
    # NO container_name (prevents scaling)
    # NO fixed host port (prevents port conflicts when scaling)
    expose:
      - "8000"     # expose to other containers, not to host
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
```

```nginx
# nginx.conf for load balancing
upstream api_servers {
    server api:8000;    # Docker DNS resolves "api" to all scaled instances
}

server {
    listen 80;
    location / {
        proxy_pass http://api_servers;
    }
}
```

---

## 28. Docker Compose Commands — All Options

### Starting and Stopping

```bash
# start services (build if needed)
docker compose up
docker compose up -d                    # detached (background)
docker compose up --build               # force rebuild images
docker compose up --no-build           # never build — fail if image missing
docker compose up --pull always         # always pull latest images
docker compose up api db               # start specific services only
docker compose up --scale api=3        # scale api to 3 instances
docker compose up --force-recreate     # recreate containers even if unchanged
docker compose up --no-recreate        # don't recreate if already running
docker compose up --abort-on-container-exit   # stop all when one exits

# stop services (SIGTERM then SIGKILL after timeout)
docker compose stop
docker compose stop api                 # stop specific service
docker compose stop --timeout 30        # 30 second grace period

# stop and remove containers, networks
docker compose down
docker compose down -v                  # also remove volumes (WARNING: data loss)
docker compose down --rmi all          # also remove built images
docker compose down --rmi local        # remove only locally built images
docker compose down --remove-orphans   # remove containers not in current compose file

# start already-created containers
docker compose start
docker compose start api

# restart services
docker compose restart
docker compose restart api
docker compose restart --timeout 10 api

# pause/unpause
docker compose pause
docker compose unpause

# kill (immediate SIGKILL)
docker compose kill
docker compose kill -s SIGINT api
```

### Building

```bash
# build all services
docker compose build
docker compose build api               # build specific service
docker compose build --no-cache        # build without cache
docker compose build --pull            # always pull base image
docker compose build --parallel        # build all in parallel

# build and push
docker compose push
docker compose push api
```

### Running One-Off Commands

```bash
# run a command in a NEW container (not the running one)
docker compose run api bash
docker compose run api python manage.py migrate
docker compose run --rm api python setup.py      # remove container after
docker compose run --no-deps api bash            # don't start dependencies
docker compose run -e DEBUG=true api bash        # set env var
docker compose run -v $(pwd)/data:/data api python process.py

# execute a command in RUNNING container
docker compose exec api bash
docker compose exec api python -c "import sys; print(sys.version)"
docker compose exec -it db psql -U user mydb
docker compose exec -u root api bash             # as root
```

### Viewing Status and Logs

```bash
# status of services
docker compose ps
docker compose ps api                   # specific service
docker compose ps --status running     # filter by status
docker compose ps --format json        # JSON output

# logs
docker compose logs
docker compose logs api                 # specific service
docker compose logs -f                  # follow all logs
docker compose logs -f api             # follow specific service
docker compose logs --tail 100         # last 100 lines
docker compose logs --tail 100 -f api  # last 100 + follow
docker compose logs -t                  # with timestamps
docker compose logs --since 1h        # last hour

# top processes
docker compose top
docker compose top api

# resource usage
docker stats $(docker compose ps -q)   # stats for all compose containers
```

### Inspecting

```bash
# list images used by compose
docker compose images

# show compose configuration (merged from all files)
docker compose config
docker compose config --services       # list service names
docker compose config --volumes        # list volume names

# show events
docker compose events
docker compose events api

# show port mappings
docker compose port api 8000           # host port mapped to container port 8000
```

### Specifying Files and Project

```bash
# use a different compose file
docker compose -f docker-compose.prod.yml up

# use multiple compose files (merged in order)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up

# set project name (changes prefix of container/network names)
docker compose -p myproject up
# or via environment variable
COMPOSE_PROJECT_NAME=myproject docker compose up

# use a different .env file
docker compose --env-file .env.production up
```

---

## 29. Real-World Compose Examples

### FastAPI + PostgreSQL + Redis + MLflow

```yaml
# docker-compose.yml — complete ML application stack

version: "3.9"

services:

  # ── FastAPI Application ───────────────────────────────────────
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: finsaight_api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:${DB_PASSWORD}@db:5432/finsaight
      REDIS_URL: redis://redis:6379/0
      MLFLOW_TRACKING_URI: http://mlflow:5000
      GROQ_API_KEY: ${GROQ_API_KEY}
      LANGSMITH_API_KEY: ${LANGSMITH_API_KEY}
    env_file:
      - .env
    volumes:
      - ml_models:/app/models
      - ./logs:/app/logs
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - frontend
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s
    logging:
      driver: json-file
      options:
        max-size: "100m"
        max-file: "5"
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"

  # ── Nginx Reverse Proxy ───────────────────────────────────────
  nginx:
    image: nginx:1.25-alpine
    container_name: finsaight_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      api:
        condition: service_healthy
    networks:
      - frontend
    restart: unless-stopped

  # ── PostgreSQL Database ───────────────────────────────────────
  db:
    image: postgres:15.2-alpine
    container_name: finsaight_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: finsaight
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d finsaight"]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 2G

  # ── Redis Cache ───────────────────────────────────────────────
  redis:
    image: redis:7.2-alpine
    container_name: finsaight_redis
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # ── MLflow Tracking Server ────────────────────────────────────
  mlflow:
    build:
      context: ./mlflow
      dockerfile: Dockerfile
    container_name: finsaight_mlflow
    ports:
      - "5000:5000"
    environment:
      MLFLOW_BACKEND_STORE_URI: postgresql://user:${DB_PASSWORD}@db:5432/mlflow
      MLFLOW_DEFAULT_ARTIFACT_ROOT: /mlflow/artifacts
    volumes:
      - mlflow_artifacts:/mlflow/artifacts
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
    profiles:
      - mlops
    restart: unless-stopped

  # ── Database Migrations (one-off task) ───────────────────────
  migrations:
    build: .
    command: python -m alembic upgrade head
    environment:
      DATABASE_URL: postgresql://user:${DB_PASSWORD}@db:5432/finsaight
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
    restart: "no"    # never restart — one-off task

  # ── Jupyter Notebook (development only) ──────────────────────
  jupyter:
    image: jupyter/scipy-notebook:python-3.10
    container_name: finsaight_jupyter
    ports:
      - "8888:8888"
    environment:
      JUPYTER_ENABLE_LAB: "yes"
    volumes:
      - .:/home/jovyan/work
      - ml_models:/home/jovyan/models
    networks:
      - backend
    profiles:
      - dev
    command: start-notebook.sh --NotebookApp.token=''

  # ── pgAdmin (database management GUI) ────────────────────────
  pgadmin:
    image: dpage/pgadmin4:7.8
    container_name: finsaight_pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - backend
    profiles:
      - tools

# ── Named Volumes ─────────────────────────────────────────────
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  ml_models:
    driver: local
  mlflow_artifacts:
    driver: local

# ── Networks ──────────────────────────────────────────────────
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: false
```

```bash
# start core services
docker compose up -d

# start with MLflow
docker compose --profile mlops up -d

# start everything for development
docker compose --profile dev --profile tools --profile mlops up -d

# run database migrations
docker compose run --rm migrations

# view all logs
docker compose logs -f

# check health
docker compose ps
```

---

## 30. Production Docker Compose

```yaml
# docker-compose.prod.yml — production overrides

services:
  api:
    image: registry.company.com/finsaight:${VERSION}
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "2.0"
          memory: 4G
        reservations:
          cpus: "0.5"
          memory: 1G
    logging:
      driver: awslogs
      options:
        awslogs-region: eu-west-1
        awslogs-group: /finsaight/api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  db:
    image: postgres:15.2-alpine
    deploy:
      resources:
        limits:
          memory: 8G
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

```bash
# deploy to production
docker compose \
    -f docker-compose.yml \
    -f docker-compose.prod.yml \
    --env-file .env.production \
    up -d

# rolling update
docker compose \
    -f docker-compose.yml \
    -f docker-compose.prod.yml \
    up -d --no-deps --build api
```

---

## 31. Cheat Sheet

```bash
# ── DOCKER ────────────────────────────────────────────────────

# Images
docker pull python:3.10-slim              # pull image
docker images                             # list images
docker build -t myapp:1.0 .              # build image
docker build --no-cache -t myapp:1.0 .  # build without cache
docker rmi myapp:1.0                     # remove image
docker image prune -a                    # remove unused images
docker tag myapp:1.0 user/myapp:1.0     # tag for registry
docker push user/myapp:1.0              # push to registry
docker history myapp:1.0                # show layers

# Containers
docker run -d -p 8000:8000 --name api myapp:1.0    # run detached
docker run -it --rm myapp:1.0 bash                  # run interactive
docker run --env-file .env myapp:1.0                # with env file
docker ps                                            # list running
docker ps -a                                         # list all
docker stop api && docker rm api                    # stop and remove
docker rm -f api                                     # force remove
docker exec -it api bash                            # shell into container
docker logs -f api                                  # follow logs
docker stats api                                    # resource usage
docker cp file.txt api:/app/                        # copy to container
docker inspect api                                  # detailed info

# Volumes
docker volume create mydata              # create volume
docker volume ls                         # list volumes
docker volume rm mydata                  # remove volume
docker volume prune                      # remove unused

# Networks
docker network create mynet              # create network
docker network ls                        # list networks
docker network connect mynet api         # connect container
docker network rm mynet                  # remove network

# System
docker system df                         # disk usage
docker system prune -a                  # clean everything unused

# ── DOCKER COMPOSE ────────────────────────────────────────────

docker compose up -d                    # start all detached
docker compose up --build -d           # rebuild and start
docker compose down                     # stop and remove
docker compose down -v                  # also remove volumes
docker compose ps                       # service status
docker compose logs -f                 # follow all logs
docker compose logs -f api             # follow one service
docker compose exec api bash           # shell into service
docker compose run --rm api python x.py  # one-off command
docker compose build                    # build all images
docker compose pull                     # pull all images
docker compose restart api             # restart one service
docker compose stop                     # stop all (keep containers)
docker compose start                    # start stopped containers
docker compose config                   # show merged config

# ── DOCKERFILE TEMPLATE ───────────────────────────────────────

# FROM python:3.10-slim
# ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
# WORKDIR /app
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl && rm -rf /var/lib/apt/lists/*
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# RUN groupadd --gid 1001 app && useradd --uid 1001 --gid app app
# USER app
# EXPOSE 8000
# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ── COMMON PORT MAPPINGS ──────────────────────────────────────
# FastAPI/Uvicorn  8000:8000
# Streamlit        8501:8501
# MLflow           5000:5000
# Jupyter          8888:8888
# PostgreSQL       5432:5432
# MySQL            3306:3306
# Redis            6379:6379
# MongoDB          27017:27017
# Elasticsearch    9200:9200
# Nginx            80:80 / 443:443
# pgAdmin          5050:80
# Grafana          3000:3000
# Prometheus       9090:9090

# ── .dockerignore TEMPLATE ────────────────────────────────────
# __pycache__/  *.pyc  .pytest_cache/
# venv/  .venv/  env/
# .env  .env.*
# data/  *.csv  *.pkl  *.h5  models/
# .git/  .gitignore
# .vscode/  .idea/
# .ipynb_checkpoints/
# .DS_Store  Thumbs.db
# *.log  logs/
```

---

*Docker docs: https://docs.docker.com*  
*Docker Compose docs: https://docs.docker.com/compose*  
*Dockerfile reference: https://docs.docker.com/engine/reference/builder*  
*Compose file reference: https://docs.docker.com/compose/compose-file*  
*Docker Hub: https://hub.docker.com*  
*Play with Docker: https://labs.play-with-docker.com*
