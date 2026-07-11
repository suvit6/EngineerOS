import os

from api.auth.routes import router as auth_router
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg import connect

load_dotenv()

app = FastAPI(title="EngineerOS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def db_health_check():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return {"status": "error", "detail": "DATABASE_URL not set"}

    try:
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1;")
                cur.fetchone()
        return {"status": "ok"}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}