from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
import os
import pathlib

# Should the uuids be stored as bytes?
BINARY_UUID = False

DB_PROVIDER_NAME = "sqlite"

DB_DRIVER_NAME = "aiosqlite"

db_name = "data"


curr_dir = pathlib.Path().resolve()

# URL for your database
db_URL = f"{DB_PROVIDER_NAME}+{DB_DRIVER_NAME}:///" + os.path.join(
    curr_dir, f"{db_name}.db"
)

engine = create_async_engine(db_URL)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


if DB_PROVIDER_NAME == "sqlite":

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
