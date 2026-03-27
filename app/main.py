from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(title="Bagguets POS API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers (se importarán y registrarán aquí)
# from app.presentation.routers import ...
# app.include_router(..., prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    from app.database import test_connection
    await test_connection()
