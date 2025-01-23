from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, \
    async_sessionmaker
from app.consts import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
