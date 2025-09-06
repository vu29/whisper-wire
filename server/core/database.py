import contextlib
from typing import Any, AsyncIterator

import pendulum
from pendulum.datetime import DateTime
from sqlalchemy import TIMESTAMP

from server.core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine, AsyncAttrs, AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column

__all__ = [
    "get_db_session",
    "sessionmanager",
    "Base",
]


class Base(DeclarativeBase, AsyncAttrs):
    created_at: MappedColumn[DateTime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: pendulum.now("UTC"),
                                                       nullable=False)
    updated_at: MappedColumn[DateTime] = mapped_column(TIMESTAMP(timezone=True), onupdate=lambda: pendulum.now("UTC"),
                                                       nullable=True)


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self.__engine = create_async_engine(host, **engine_kwargs)
        self.__sessionmaker = async_sessionmaker(autocommit=False, bind=self.__engine)

    @property
    def engine(self) -> AsyncEngine | None:
        return self.__engine

    async def close(self):
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.__engine.dispose()

        self.__engine = None
        self.__sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.__sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self.__sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.db_url, {"echo": settings.echo_sql})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
