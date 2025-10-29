from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

# Create an asynchronous SQLAlchemy engine using the database URL from settings.
engine =  create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

# Create an asynchronous SQLAlchemy sessions for database operations.
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)