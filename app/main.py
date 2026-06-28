import os
import time
from fastapi import FastAPI
import psycopg2
from redis import Redis

app = FastAPI(title="Multi-Tier FastAPI App")

# Environment variables injected by Kubernetes
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "password")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Tier FastAPI App on Minikube!"}

@app.get("/healthz")
def health_check():
    status = {"status": "healthy", "database": "disconnected", "redis": "disconnected"}
    
    # Check PostgreSQL
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, connect_timeout=3)
        conn.close()
        status["database"] = "connected"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        status["status"] = "unhealthy"

    # Check Redis
    try:
        r = Redis(host=REDIS_HOST, port=6379, socket_timeout=3)
        if r.ping():
            status["redis"] = "connected"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"
        status["status"] = "unhealthy"

    return status