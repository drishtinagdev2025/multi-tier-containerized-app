Multi-Tier FastAPI Application on Kubernetes

This repository contains a containerized 3-Tier Architecture application structured for local deployment using Kubernetes. The infrastructure features a FastAPI backend web service tightly integrated with a Redis caching layer and a PostgreSQL database.

🏗️ Architecture Overview

Frontend/API Tier: A lightweight FastAPI python container handling request routing and business logic.

Caching Tier: An in-memory Redis instance optimizing volatile session and cache data transactions.

Data Tier: A relational PostgreSQL instance managing persistent storage records.

🛠️ Prerequisites
Ensure the following tools are installed locally and added to your system's PATH:

Docker Desktop, Minikube, or Rancher Desktop

kubectl (Kubernetes CLI)

Python 3.11+ (For local debugging)

🚀 Setup & Deployment Steps

1. your local Kubernetes engine

2. Build the Backend Docker Image

docker build -t local/fastapi-app:latest .

3. Apply Kubernetes Configurations

# 1. Spin up the Data Tier
kubectl apply -f k8s/postgres-deployment.yaml

# 2. Spin up the Cache Tier
kubectl apply -f k8s/redis-deployment.yaml

# 3. Spin up the Application Tier
kubectl apply -f k8s/fastapi-deployment.yaml

4. Verify Resources and Deploy Status

kubectl get pods,svc

5. Portforward the app service and verify the endpoints

Root Route (/): Returns a welcome handshake string verification.

Health Checks (/healthz): Returns a real-time system check assessing direct network socket connectivity to Redis and PostgreSQL backend layers:

JSON
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}