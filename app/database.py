from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c: None)
        print("DB connection OK")
    except Exception as e:
        print(f"DB connection failed: {e}")
        raise
