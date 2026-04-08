from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.presentation.routers import (
    auth,
    products,
    ingredients,
    expenses,
    workers,
    promotions,
    sales,
    cash_register,
    reports,
)

app = FastAPI(title="Bagguets POS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(products.router, prefix=API_PREFIX)
app.include_router(ingredients.router, prefix=API_PREFIX)
app.include_router(expenses.router, prefix=API_PREFIX)
app.include_router(workers.router, prefix=API_PREFIX)
app.include_router(promotions.router, prefix=API_PREFIX)
app.include_router(sales.router, prefix=API_PREFIX)
app.include_router(cash_register.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)

@app.on_event("startup")
async def startup_event():
    from app.database import test_connection
    await test_connection()
