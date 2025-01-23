import asyncio
from app.db.session import async_engine
from app.db.models import Base


async def init_db():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


if __name__ == "__main__":
    asyncio.run(init_db())
