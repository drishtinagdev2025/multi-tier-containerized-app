import os
import psycopg2
from redis import Redis
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Multi-Tier FastAPI App")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Tier FastAPI App on Minikube!"}

@app.get("/healthz")
def health_check():
    status_report = {"status": "healthy", "database": "disconnected", "redis": "disconnected"}
    is_unhealthy = False
    
    # Fetch environment variables directly inside the function scope
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD", "password")
    redis_host = os.getenv("REDIS_HOST", "localhost")
    
    # Check PostgreSQL
    try:
        conn = psycopg2.connect(
            host=db_host, 
            database=db_name, 
            user=db_user, 
            password=db_pass, 
            connect_timeout=3
        )
        conn.close()
        status_report["database"] = "connected"
    except Exception as e:
        status_report["database"] = f"error: {str(e)}"
        status_report["status"] = "unhealthy"
        is_unhealthy = True

    # Check Redis
    try:
        r = Redis(host=redis_host, port=6379, socket_timeout=3)
        if r.ping():
            status_report["redis"] = "connected"
    except Exception as e:
        status_report["redis"] = f"error: {str(e)}"
        status_report["status"] = "unhealthy"
        is_unhealthy = True

    # Trigger HTTP 503 if dependencies fail
    if is_unhealthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=status_report
        )

    return status_report