from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import os
import pathlib

db_name = "test_data"

curr_dir = pathlib.Path().resolve()

# URL for your test database
db_URL = "sqlite+aiosqlite:///" + os.path.join(curr_dir, f"{db_name}.db")

engine = create_async_engine(db_URL, echo=True)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
