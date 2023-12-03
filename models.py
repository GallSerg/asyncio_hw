import os

from sqlalchemy import JSON, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "asyncio_app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    # json: Mapped[dict] = mapped_column(JSON, nullable=True)
    name: Mapped[str] = mapped_column(
        String(150), unique=True, index=True, nullable=True
    )
    birth_year: Mapped[str] = mapped_column(
        String(15), unique=False, index=True, nullable=True
    )
    eye_color: Mapped[str] = mapped_column(
        String(20), unique=False, index=True, nullable=True
    )
    films: Mapped[str] = mapped_column(
        String(500), unique=False, index=False, nullable=True
    )
    gender: Mapped[str] = mapped_column(
        String(15), unique=False, index=True, nullable=True
    )
    hair_color: Mapped[str] = mapped_column(
        String(20), unique=False, index=True, nullable=True
    )
    height: Mapped[str] = mapped_column(
        String(15), unique=False, index=False, nullable=True
    )
    homeworld: Mapped[str] = mapped_column(
        String(50), unique=False, index=False, nullable=True
    )
    mass: Mapped[str] = mapped_column(
        String(15), unique=False, index=False, nullable=True
    )
    skin_color: Mapped[str] = mapped_column(
        String(20), unique=False, index=True, nullable=True
    )
    species: Mapped[str] = mapped_column(
        String(500), unique=False, index=False, nullable=True
    )
    starships: Mapped[str] = mapped_column(
        String(500), unique=False, index=False, nullable=True
    )
    vehicles: Mapped[str] = mapped_column(
        String(500), unique=False, index=False, nullable=True
    )


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
