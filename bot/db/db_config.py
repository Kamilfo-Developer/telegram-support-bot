from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
import pathlib

# SQLAlchemy base
Base = declarative_base()


db_name = "data"

curr_dir = pathlib.Path().resolve()

# URL for your database
db_URL = "sqlite+aiosqlite:///" + os.path.join(curr_dir, f"{db_name}.db")

engine = create_async_engine(db_URL)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
