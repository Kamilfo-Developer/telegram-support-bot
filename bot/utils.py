from bot.db.db_config import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    with async_session() as session:
        return session
