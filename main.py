import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import contact, auth
from database import init_db

app = FastAPI(title="Master API — All Projects")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "https://www.tradiemigration.com",
        "https://tradiemigration.com",
        "https://tradie-migration.vercel.app",
        "https://digital-me-three.vercel.app",
        "https://apd-rehear.vercel.app",
    ],
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact.router)
app.include_router(auth.router)

@app.on_event("startup")
def bootstrap_database():
    try:
        init_db()
    except Exception as e:
        print(f"DB init failed: {e}")

@app.get("/")
def root():
    return {
        "status": "ok",
        "api": "master-backend",
        "message": "Backend is running.",
        "health": "/health",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "ok", "api": "master-backend"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)